'''
    logger.py
'''
import logging
from pathlib import Path
from typing import Optional

from api_pipe import config
from rich.logging import RichHandler

class ClosingFileHandler(logging.FileHandler):
    def emit(self, record):
        super().emit(record)
        self.close()

def stdout(
        unique_name: str,
        log_level: int,
        log_words_to_highlight: list,
        log_to_file: Optional[Path] = None
    ) -> logging.Logger:
    '''
        Sets up a logger that logs to stdout

        Uses RichHandler to pretty print logs

        When log_level is DEBUG, also logs to a file in log_to_file.
    '''
    #stdout handler
    stdout_handler = RichHandler(
        show_time=config.logger_show_time,
        keywords=[w.lower() for w in log_words_to_highlight] + \
                 [w.upper() for w in log_words_to_highlight] + \
                 [w.capitalize() for w in log_words_to_highlight]
    )
    stdout_handler.setFormatter(logging.Formatter(
        config.logger_formatter_stdout
    ))

    #file handler
    if log_to_file is not None:
        file_handler = ClosingFileHandler(log_to_file)
        file_handler.setFormatter(logging.Formatter(
            config.logger_formatter_stdout_in_file
        ))


    #config logger
    logger = logging.getLogger(unique_name)
    logger.setLevel(log_level)

    #add handlers
    logger.addHandler(stdout_handler)

    if log_to_file is not None:
        logger.addHandler(file_handler)

    return logger
