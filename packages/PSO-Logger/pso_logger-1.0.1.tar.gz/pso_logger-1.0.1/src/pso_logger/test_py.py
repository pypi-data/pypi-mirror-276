from pso_logging import ConsoleJsonLogger
import logging

logger = ConsoleJsonLogger(log_level=logging.DEBUG)
logger.log_message("INFO", "This is a log level message")
