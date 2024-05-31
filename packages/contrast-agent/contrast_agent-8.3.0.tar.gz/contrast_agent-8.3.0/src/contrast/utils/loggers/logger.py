# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import os
import socket
import ssl
import sys
import time

import logging as stdlib_logging
import logging.handlers as stdlib_logging_handlers
from typing import Any, Dict, NamedTuple, Optional, Tuple, TypedDict

import contrast
from contrast.assess_extensions import cs_str
from contrast.utils.decorators import fail_loudly
from contrast.utils.loggers.structlog import init_structlog
from contrast.utils.configuration_utils import get_hostname
from contrast.utils.namespace import Namespace
from contrast.configuration.config_option import CONTRAST_UI_SRC, DEFAULT_VALUE_SRC

from contrast.utils.string_utils import ensure_string
from contrast_vendor import structlog

from . import DEFAULT_LOG_LEVEL, DEFAULT_PROGNAME, LOGGER_NAME

STDOUT = "STDOUT"
STDERR = "STDERR"


class module(Namespace):
    initialized: bool = False
    cef_security_logger: Optional[stdlib_logging.Logger] = None
    syslog_logger: Optional["SysLogger"] = None


def setup_basic_agent_logger(level=stdlib_logging.INFO):
    """
    Setup a logger without any user-supplied configuration, with defaults:
        1. log to stdout
        2. log in INFO level
        3. with default progname

    The logger created here is expected to be overridden with config values
    provided later on in the middleware creation cycle.
    """
    if not module.initialized:
        logger = stdlib_logging.getLogger(LOGGER_NAME)
        logger.addHandler(stdlib_logging.StreamHandler(sys.stdout))
        _set_handler(logger, "STDOUT", DEFAULT_PROGNAME)
        logger.setLevel(level)

        init_structlog()
        module.initialized = True

    return structlog.getLogger(LOGGER_NAME)


def setup_agent_logger(config):
    """
    Initialize the agent logger with configurations.
    :param config: instance of AgentConfig or dict
    :return: None
    """
    if config.get_value("agent.logger.stdout"):
        path = STDOUT
    elif config.get_value("agent.logger.stderr"):
        path = STDERR
    else:
        path = config.get_value("agent.logger.path")
    level = config.get_value("agent.logger.level").upper()

    logger = stdlib_logging.getLogger(LOGGER_NAME)

    _set_logger_info(logger, config, path, level)

    cs_str.initialize_logger(structlog.getLogger(LOGGER_NAME))


class CEFFormatter(stdlib_logging.Formatter):
    ATTACK_MSG_FMT = (
        f"%(asctime)s {get_hostname()} CEF:0|Contrast Security|Contrast Agent Python|{contrast.__version__}|"
        "SECURITY|%(message)s|%(level)s|pri=%(rule_id)s src=%(source_ip)s spt=%(source_port)s "
        "request=%(request_url)s requestMethod=%(request_method)s app=%(application)s "
        "outcome=%(outcome)s"
    )

    def __init__(self):
        super().__init__(CEFFormatter.ATTACK_MSG_FMT)

    def formatTime(self, record, datefmt=None) -> str:
        ct = self.converter(record.created)
        t = time.strftime("%b %d %Y %H:%M:%S", ct)
        z = time.strftime("%z", ct)
        s = "%s.%03d%s" % (t, record.msecs, z)
        return s


def setup_security_logger(cfg):
    config = cfg if cfg else {}

    if not config.get_value("protect.enable"):
        return

    path = config.get_value("agent.security_logger.path")
    level = config.get_value("agent.security_logger.level").upper()

    logger = stdlib_logging.getLogger("contrast-security-logger")

    _set_level(logger, level)

    handler = _get_handler(path)
    handler.setFormatter(CEFFormatter())
    logger.addHandler(handler)
    module.cef_security_logger = logger


def _unescaped_protect_rule_msg(rule_name, outcome, evaluation):
    input_type = evaluation.input_type.cef_string(evaluation.key) if evaluation else "-"
    input_value = (
        ensure_string(evaluation.value, errors="replace") if evaluation else "-"
    )
    if outcome == "exploited":
        if not evaluation:
            return f"An effective attack was detected against {rule_name}"
        return f"The {input_type} had a value that successfully exploited {rule_name} - {input_value}"
    if outcome in ("blocked", "ineffective"):
        if not evaluation:
            return f"An unsuccessful attack was detected against {rule_name}"
        return f"The {input_type} had a value that matched a signature for, but did not successfully exploit {rule_name} - {input_value}"
    if outcome == "suspicious":
        if not evaluation:
            return f"Suspicious activity indicates a potential attack using {rule_name} - {input_value}"
        return f"The {input_type} included a potential attack value that was detected as suspicious using {rule_name} - {input_value}"
    raise ValueError(f"Unknown outcome: {outcome}")


@fail_loudly("Failed to log attack event to security loggers")
def security_log_attack(attack, evaluation, app_name):
    """
    Logs a security event to the CEF security logger and syslog logger.

    Virtual patches, IP denylist and bot blocker activities are not yet supported.
    """
    rule_name = attack.rule_id
    outcome = attack.report_result()
    msg = _escape_prefix(_unescaped_protect_rule_msg(rule_name, outcome, evaluation))

    if not app_name:
        app_name = "-"
    ip = port = url = method_name = "-"

    if (context := contrast.CS__CONTEXT_TRACKER.current()) is not None:
        ip = context.request.client_addr or "-"
        port = context.request.host_port
        method_name = context.request.method
        url = context.request.path

    log_context = _escape_metadata(
        {
            "level": "WARN",
            "rule_id": rule_name,
            "source_ip": ip,
            "source_port": port,
            "request_url": url,
            "request_method": method_name,
            "application": app_name,
            "outcome": outcome.upper(),
        }
    )

    if module.cef_security_logger:
        module.cef_security_logger.warning(msg, extra=log_context)
    _syslog_msg(msg, log_context, outcome, perimeter=attack.perimeter_blocked)


def _escape_prefix(msg: str):
    # Order matters here. Escaping `|` before `\` would result in double escaping.
    return msg.replace("\\", r"\\").replace("|", r"\|")


def _escape_metadata(metadata: Dict[str, str]):
    return {
        k: v.replace("=", r"\=").replace("\n", r"\n").replace("\r", r"\r")
        for k, v in metadata.items()
    }


def _syslog_msg(msg, log_context, outcome, perimeter):
    syslogger = module.syslog_logger
    if not syslogger:
        # syslog logger isn't configured.
        return

    outcome = outcome.lower()
    if perimeter and outcome == "blocked":
        outcome = "blocked_perimeter"
    syslogger.logger.warning(
        msg, extra={**log_context, "_severity": syslogger.outcome_to_severity[outcome]}
    )


class SysLogger(NamedTuple):
    logger: stdlib_logging.Logger
    outcome_to_severity: Dict[str, str]


class SysLogHandlerConfig(TypedDict):
    address: Tuple[str, int]
    facility: int
    socktype: socket.SocketType
    secure: bool
    protect_priorities: Dict[str, str]


class SecureSysLogHandler(stdlib_logging_handlers.SysLogHandler):
    """
    A SysLogHandler that logs security events to syslog.

    This handler extends SysLogHandler to use SSL/TLS if the secure option is
    set to True. It also adds security event outcomes as log levels in the
    standard logging module.
    """

    _valid_severities = {
        "ALERT",
        "CRITICAL",
        "ERROR",
        "WARNING",
        "NOTICE",
        "INFO",
        "DEBUG",
    }

    @classmethod
    def severity(cls, s: str):
        if s.upper() not in cls._valid_severities:
            raise ValueError(f"Invalid syslog severity: {s}")
        return s.lower()

    _valid_protocols = {"UDP", "TCP", "TCP_TLS"}

    @classmethod
    def protocol(cls, p: str):
        if p.upper() not in cls._valid_protocols:
            raise ValueError(f"Invalid syslog protocol: {p}")
        return p.upper()

    def __init__(self, *args, secure=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.append_nul = False
        if secure:
            ctx = ssl.create_default_context()
            self.socket = ctx.wrap_socket(self.socket, server_hostname=self.address[0])

        # Store the config so we can reference it later and potentially
        # avoid reconfiguring the logger if the config hasn't changed.
        self.config = {
            "args": args,
            "kwargs": {
                **kwargs,
                "secure": secure,
            },
        }

    def format(self, record) -> str:
        # HACK: The SysLogHandler extension capabilities are based on
        # adding custom logging levels, which is very difficult to do
        # safely as a library. Levels need integers and there's always
        # a chance the integer we choose will conflict with another
        # library. We'd prefer to avoid introducing log levels.
        #
        # Instead, we use this format call as a hook at the start of
        # the emit method to overwrite the levelname since levelname
        # is the only way to set the message priority.
        record.levelname = record.__dict__["_severity"]
        return super().format(record)

    def mapPriority(self, levelName: str) -> str:
        # bypass the priorityMap conversion.
        return levelName


DEFAULT_SYSLOG_PORTS = {
    "UDP": 514,
    "TCP": 601,
    "TCP_TLS": 6514,
}


def configure_syslog_logger(config) -> bool:
    """
    Configures the syslog logger with AgentConfig. This function can be called
    multiple times to reconfigure the logger with new configurations. The
    return value indicates whether the logger was reconfigured.

    The syslog logger uses the standard logging module to send messages to an
    adapted SysLogHandler.
    """
    if not config.get_value("protect.enable") or not config.get_value(
        "agent.security_logger.syslog.enable"
    ):
        return close_syslog_logger()

    outcomes_to_severities: Dict[str, str] = {
        "blocked": config.get_value("agent.security_logger.syslog.severity_blocked"),
        "exploited": config.get_value(
            "agent.security_logger.syslog.severity_exploited"
        ),
        "ineffective": config.get_value("agent.security_logger.syslog.severity_probed"),
        "blocked_perimeter": config.get_value(
            "agent.security_logger.syslog.severity_blocked_perimeter"
        ),
        "suspicious": config.get_value(
            "agent.security_logger.syslog.severity_suspicious"
        ),
    }
    new_handler_config = _syslog_handler_config(config)

    logger, changed = _configure_syslog_std_logger(new_handler_config)
    module.syslog_logger = SysLogger(logger, outcomes_to_severities)
    return changed


def _configure_syslog_std_logger(config) -> Tuple[stdlib_logging.Logger, bool]:
    logger = (
        module.syslog_logger.logger
        if module.syslog_logger
        else stdlib_logging.getLogger("contrast-syslog-logger")
    )
    previous_handler = None
    if (
        logger.handlers
        and (handler := logger.handlers[0])
        and isinstance(handler, SecureSysLogHandler)
    ):
        if handler.config == {"args": tuple(), "kwargs": config}:
            # The configuration hasn't changed. Continue to use the existing
            # handler.
            return logger, False

        # previous_handler will be closed and removed after the new handler
        # is added. This ordering prevents dropping messages.
        #
        # A message could be written to both the previous_handler and the
        # latest handler. This is arguably duplication, but we can counter
        # by calling it redundancy, and this implementation side-steps the
        # need for additional locking or other synchronization.
        #
        # We could be finer grained in the condition above so that we keep
        # the existing connection in the address hasn't changed, but syslog
        # configurations from TeamServer don't happen frequently (at most once
        # per server settings polling period), so we'll keep it simple.
        previous_handler = handler

    handler = SecureSysLogHandler(**config)
    handler.setFormatter(CEFFormatter())

    logger.addHandler(handler)
    if previous_handler:
        previous_handler.close()
        logger.removeHandler(previous_handler)

    return logger, True


def _syslog_handler_config(config) -> Dict[str, Any]:
    protocol = config.get_value("agent.security_logger.syslog.protocol")
    ip = config.get_value("agent.security_logger.syslog.ip")
    port = config.get_value(
        "agent.security_logger.syslog.port"
    ) or DEFAULT_SYSLOG_PORTS.get(protocol)
    facility = config.get_value("agent.security_logger.syslog.facility")
    socket_type = socket.SOCK_DGRAM if protocol == "UDP" else socket.SOCK_STREAM
    return {
        "address": (ip, port),
        "facility": facility,
        "socktype": socket_type,
        "secure": protocol == "TCP_TLS",
    }


def close_syslog_logger():
    """
    Closes the syslog logger if it is currently enabled.

    Returns False if the logger is already disabled.
    """
    syslogger = module.syslog_logger
    if not syslogger:
        return False
    handlers = syslogger.logger.handlers
    for handler in handlers:
        handler.close()
    handlers.clear()
    return True


def reset_agent_logger(log_path, log_level, config):
    """
    Reset agent logger path and/or level after the logger has already been created.

    Also note that progname is never reset so we use the one already set to the logger.

    :return: Bool if any logger value is reset
    """
    logger = stdlib_logging.getLogger(LOGGER_NAME)

    is_reset = False
    current_path_option = config.get("agent.logger.path") if config else None
    # A configuration path can be changed if the config is unset or we're not set directly to STDOUT or STDERR
    changeable_path = not config or not (
        config.get_value("agent.logger.stdout")
        or config.get_value("agent.logger.stderr")
    )
    if log_path:
        need_update = current_path_option is None or (
            log_path != current_path_option.value()
            and current_path_option.source() in (CONTRAST_UI_SRC, DEFAULT_VALUE_SRC)
            and changeable_path
        )
        if current_path_option:
            current_path_option.ui_value = log_path
        if need_update:
            current_handler = logger.handlers[0]
            progname = current_handler.filters[0].progname
            _set_handler(logger, log_path, progname)
            # print so it shows up in STDOUT
            print(f"Contrast Agent Logger updated path to {log_path}")
            is_reset = True

    current_level_option = config.get("agent.logger.level") if config else None
    if log_level:
        need_update = current_level_option is None or (
            log_level != current_level_option.value()
            and current_level_option.source() in (CONTRAST_UI_SRC, DEFAULT_VALUE_SRC)
        )
        if current_level_option:
            current_level_option.ui_value = log_level
        if need_update:
            _set_level(logger, log_level)

            # print so it shows up in STDOUT
            print(f"Contrast Agent Logger updated level to {log_level}")
            # Avoid circular import
            from contrast.agent.agent_lib import update_log_options

            if update_log_options(log_level):
                print(f"Contrast Agent Lib Logger updated level to {log_level}")
            is_reset = True
    return is_reset


def _set_logger_info(logger, config, path, level):
    progname = config.get_value("agent.logger.progname")

    _set_handler(logger, path, progname)
    _set_level(logger, level)


def _set_handler(logger, path, progname):
    """
    A logger's handler is what determines where the log records will be printed to
    and what format they will have.

    To reset a handler, we delete the existing handlers and create a new one.

    CONTRAST-39746 defined the datetime format as ISO_8601. The one here is
    without ms as the logger doesn't natively support both ms and time zone at this time.
    """
    handler = _get_handler(path)
    program_filter = AgentFilter(progname=progname)
    handler.addFilter(program_filter)

    # empty all handlers so there is only one stdlib_logging handler with this config
    logger.handlers = []
    logger.addHandler(handler)


def _get_handler(path):
    if path == STDOUT:
        handler = stdlib_logging.StreamHandler(sys.stdout)
    elif path == STDERR:
        handler = stdlib_logging.StreamHandler(sys.stderr)
    else:
        try:
            if dirname := os.path.dirname(path):
                os.makedirs(dirname, exist_ok=True)
            handler = stdlib_logging.FileHandler(path)
        except Exception as e:
            print(e, file=sys.stderr)
            # path could be '' or None
            handler = stdlib_logging.StreamHandler()

    return handler


def _set_level(logger, level: str) -> None:
    if level.upper() == "TRACE":
        level = "DEBUG"
        print("Contrast Python Agent: TRACE logging is equivalent to DEBUG")
    try:
        logger.setLevel(level)
    except ValueError:
        # this fails validation if the level is an invalid value
        logger.setLevel(DEFAULT_LOG_LEVEL)


class AgentFilter(stdlib_logging.Filter):
    def __init__(self, progname=None):
        self.progname = progname
        super().__init__()

    def filter(self, record):
        record.progname = self.progname
        return super().filter(record)
