import logging
from datetime import datetime
from pathlib import Path

class LoggerConfig:
    """Enhanced Logger Configuration with rotation and multiple handlers."""
    
    def __init__(self, logger_name="PDFQueryLogger", log_level=logging.DEBUG):

        self.logger_name = logger_name
        self.log_level = log_level
        self.log_dir = Path.cwd() / "logs"
        self.setup_directories()
        self.logger = self.setup_logger()


    def setup_directories(self):
        """Create Log Directory Structure."""
        self.log_dir.mkdir(exist_ok=True)

    def setup_logger(self):
        """Configure Logger with file rotation and console output."""
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(self.log_level)

        logger.handlers.clear()

        log_filename = f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.log"
        file_handler = logging.handlers.RotatingFileHandler(
            filename=self.log_dir / log_filename,
            maxBytes=10 * 1024 * 1024,
            backupCount=10,
            encoding='utf-8'
        )

        console_handler = logging.StreamHandler()

        file_formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(funcName)s() | %(message)s',
            datefmt='%d-%m-%Y %H:%M:%S'
        )

        console_formatter = logging.Formatter(
            '%(levelname)-8s | %(message)s'
        )

        file_handler.setFormatter(file_formatter)
        console_handler.setFormatter(console_formatter)

        file_handler.setLevel(logging.DEBUG)
        console_handler.setLevel(logging.INFO)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger
    
    def get_logger(self):
        """Get COnfigured Logger Instance."""
        return self.logger
    
    def log_exception(self, msg="An Error Occurred"):
        """Log exception with full trackback."""
        self.logger.exception(msg)
    
    def log_performance(self, func_name, execution_time):
        """Log performance metrics."""
        self.logger.info(f"PERFORMANCE | {func_name} executed in {execution_time:.4f}s")


log_config = LoggerConfig("PDFQueryLogger")
logger = log_config.get_logger()