import os
from logzero import logger, setup_logger
from logging.handlers import TimedRotatingFileHandler


class DailyRotatingLogger:
    def __init__(self, log_directory: str, log_filename: str, log_level='info'):
        self.log_directory = log_directory
        self.log_filename = log_filename
        self.log_level = log_level.upper()

        # Ensure the log directory exists
        os.makedirs(self.log_directory, exist_ok=True)

        # Full log file path
        log_file_path = os.path.join(self.log_directory, self.log_filename)

        # Create a TimedRotatingFileHandler
        handler = TimedRotatingFileHandler(log_file_path, when="midnight", interval=1)
        handler.suffix = "%Y-%m-%d.log"  # Log file suffix

        # Create a logger with the handler
        self.logger = setup_logger(name="daily_logger", logfile=log_file_path, level=self.log_level)
        self.logger.addHandler(handler)

    def get_logger(self):
        return self.logger
