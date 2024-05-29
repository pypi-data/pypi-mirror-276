import logging
import os
from .styles import styles, reset

class console:
    log_enabled = False
    logger = None
    log_file = 'messages.log'

    @classmethod
    def enable_logging(cls, log_file: str = 'messages.log', log_level: str = 'INFO') -> None:
        cls.log_enabled = True
        cls.log_file = log_file
        cls.logger = logging.getLogger('VerboseTerminal')
        numeric_level = getattr(logging, log_level.upper(), logging.INFO)
        cls.logger.setLevel(numeric_level)
        handler = logging.FileHandler(cls.log_file)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        cls.logger.addHandler(handler)
        # Define custom log level for success
        logging.addLevelName(25, 'SUCCESS')
        setattr(cls.logger, 'success', lambda message, *args: cls.logger._log(25, message, args))
        logging.addLevelName(5, 'LOG')
        setattr(cls.logger, 'log', lambda message, *args: cls.logger._log(5, message, args))

    @classmethod
    def disable_logging(cls):
        if cls.logger:
            handlers = cls.logger.handlers[:]
            for handler in handlers:
                handler.close()
                cls.logger.removeHandler(handler)
        cls.log_enabled = False
        cls.logger = None

    @classmethod
    def view_logs(cls) -> str:
        if not cls.log_enabled:
            cls.critical("Logging is not enabled. No logs to clear.")
        with open(cls.log_file, 'r') as file:
            return file.read()

    @classmethod
    def clear_logs(cls) -> None:
        if not cls.log_enabled:
            cls.critical("Logging is not enabled. No logs to clear.")
        open(cls.log_file, 'w').close()

    @classmethod
    def save_logs(cls, destination: str) -> None:
        if not cls.log_enabled:
            cls.critical("Logging is not enabled. No logs to clear.")
        with open(cls.log_file, 'r') as src:
            content = src.read()
        with open(destination, 'w') as dest:
            dest.write(content)

    @classmethod
    def _log_message(cls, message: str, level: str = 'info') -> None:
        if cls.log_enabled and cls.logger:
            if hasattr(cls.logger, level):
                log_method = getattr(cls.logger, level, cls.logger.info)
                log_method(message)

    @classmethod
    def _print_message(cls, message: str, verbose: bool = True, style: str = 'log') -> None:
        if verbose:
            if style in styles:
                print(f'{styles[style]}{message}{reset}')
            else:
                print(message)

    @classmethod
    def log(cls, message: str, verbose: bool = True) -> None:
        cls._print_message(message, verbose, 'log')
        cls._log_message(message, 'log')

    @classmethod
    def debug(cls, message: str, verbose: bool = True) -> None:
        cls._print_message(message, verbose, 'debug')
        cls._log_message(message, 'debug')

    @classmethod
    def info(cls, message: str, verbose: bool = True) -> None:
        cls._print_message(message, verbose, 'info')
        cls._log_message(message, 'info')
    
    @classmethod
    def success(cls, message: str, verbose: bool = True) -> None:
        cls._print_message(message, verbose, 'success')
        cls._log_message(message, 'success')

    @classmethod
    def warning(cls, message: str, verbose: bool = True) -> None:
        cls._print_message(message, verbose, 'warning')
        cls._log_message(message, 'warning')

    @classmethod
    def error(cls, message: str, verbose: bool = True) -> None:
        cls._print_message(message, verbose, 'error')
        cls._log_message(message, 'error')

    @classmethod
    def critical(cls, message: str, verbose: bool = True) -> None:
        cls._print_message(message, verbose, 'critical')
        cls._log_message(message, 'critical')