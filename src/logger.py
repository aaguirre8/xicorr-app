import logging
import os
from typing import Optional


class LogRecorder:
    """A utility class for application-wide logging implemented as a Singleton.

    This class configures and provides a logger to record application logs. It ensures a tmp directory exists for file-based logging.

    Attributes:
        name (str): The name of the logger, typically the module name.
        level (int): The logging level, defaults to logging.INFO.
        filename (Optional[str]): The filename for file-based logging, defaults to None. Assumes a tmp directory.

    Usage example:
        logger = LogRecorder(__name__, logging.INFO, "app.log")
        logger.log(logging.INFO, "This is an info message.")
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LogRecorder, cls).__new__(cls)
            # Initialize the instance once
            cls._instance._initialized = False
        return cls._instance

    def __init__(
        self,
        name: str,
        level: int = logging.INFO,
        filename: Optional[str] = None,
        session_id: Optional[str] = None,
    ):
        if not self._initialized:
            self.name = name
            self.level = level
            self.filename = filename
            self.logger = logging.getLogger(name)
            self.logger.setLevel(level)
            self._configure_logging()
            self._initialized = True
            self.session_id = session_id

    def _ensure_tmp_directory(self) -> str:
        """Ensures that a tmp directory exists for logging."""
        tmp_dir = "tmp_logs"
        os.makedirs(tmp_dir, exist_ok=True)
        return tmp_dir

    def _configure_logging(self) -> None:
        """Configures the logger with a console and/or file handler based on initialization parameters."""
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        # Console handler
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        # File handler, if filename is provided
        if self.filename:
            tmp_dir = self._ensure_tmp_directory()
            file_path = os.path.join(tmp_dir, self.filename)
            fh = logging.FileHandler(file_path, mode="w")
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

    def log(self, level: int, msg: str) -> None:
        """Logs a message with the specified logging level."""
        if self.session_id:
            msg = f"session_id: {self.session_id} - {msg}"
        self.logger.log(level, msg)

    def info(self, msg: str, *args, **kwargs) -> None:
        if self.session_id:
            msg = f"session_id: {self.session_id} - {msg}"
        self.logger.info(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs) -> None:
        if self.session_id:
            msg = f"session_id: {self.session_id} - {msg}"
        self.logger.error(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs) -> None:
        if self.session_id:
            msg = f"session_id: {self.session_id} - {msg}"
        self.logger.warning(msg, *args, **kwargs)


def logger_dpf():
    """
    Dependency Provider Function (DPF) for the LogRecorder class.
    """
    return LogRecorder(__name__, logging.INFO, "app.log")
