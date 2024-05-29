import logging
import json
from datetime import datetime, timezone
import inspect


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        frame = inspect.stack()[1]
        filename = frame.filename.split("/")[-1]
        utc_time = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()
        return json.dumps(
            {
                "timestamp": self.formatTime(record),
                "utc_time": utc_time,
                "level": record.levelname,
                "message": record.msg,
                "filename": filename,
            }
        )


class ConsoleJsonLogger:
    def __init__(self, log_level: int = logging.INFO) -> None:
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

        # Create a StreamHandler
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(log_level)

        # Set up a custom JSON formatter
        formatter = JsonFormatter()
        stream_handler.setFormatter(formatter)

        # Add the handler to the logger
        self.logger.addHandler(stream_handler)

    def log_message(self, level: str, message: str) -> None:
        """Log a message at the specified level."""
        if hasattr(self.logger, level):
            getattr(self.logger, level)(message)
        else:
            self.logger.error(f"Invalid log level: {level}")
