#
# Copyright (C) 2024 RomanLabs, Rafael Roman Otero
# This file is part of RLabs Mini CLI
#
# RLabs Mini CLI is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RLabs Mini CLI is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with RLabs Mini CLI. If not, see <http://www.gnu.org/licenses/>.
#
'''
    logger.py
'''
import logging
from rich.logging import RichHandler
from rich.traceback import install

def enable_pretty_tracebacks() -> None:
    '''
        Enable Pretty Traceback

        Uses rich to print pretty tracebacks
    '''
    install()

def stdout(
        name: str,
        log_level: int,
        format: str,
        show_time: bool,
        words_to_highlight: list[str]
    ) -> logging.Logger:
    '''
        Sets up a logger that logs to stdout

        Uses RichHandler to pretty print logs
    '''

    handler = RichHandler(
        show_time=show_time,
        keywords=[w.lower() for w in words_to_highlight] + \
                 [w.upper() for w in words_to_highlight] + \
                 [w.capitalize() for w in words_to_highlight]
    )

    logger = CustomLogger(name)
    logger.setLevel(log_level)
    formatter = logging.Formatter(format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

class CustomLogger(logging.Logger):
    '''
        Extends the logging.Logger class
        with  custom methods
    '''
    def flush(self) -> None:
        '''
            Flush

            Flushes the logger
        '''
        for handler in self.handlers:
            handler.flush()

