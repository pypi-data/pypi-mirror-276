# Copyright (C) 2024 RomanLabs, Rafael Roman Otero
# This file is part of API Pipe.
#
# API Pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# API Pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with API Pipe. If not, see <http://www.gnu.org/licenses/>.

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

        When log_level is DEBUG, also logs to a file in log_to_file
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
