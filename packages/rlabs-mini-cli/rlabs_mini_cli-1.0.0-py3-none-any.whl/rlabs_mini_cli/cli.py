#
# Copyright (C) 2024 RomanLabs, Rafael Roman Otero
# This file is part of RLabs Mini CLI
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
#
'''
    CLI
'''
import logging
import argparse
from typing import Optional
from typing import Callable
from typing import List
from typing import Any
from typing import TypedDict
from dataclasses import dataclass
from dataclasses import field
from rich.console import Console


from rlabs_mini_cli.error import NoAppDefined
from rlabs_mini_cli import logger
from rlabs_mini_cli import args
from rlabs_mini_cli import envvars

def _default_app(
    args: argparse.Namespace,
    envs: envvars.EnvVars,
    logger: logging.Logger
):
    '''
        Default App

        Runs when no app is defined
    '''
    raise NoAppDefined()

_app: Callable = _default_app

def app(func):
    '''
        App decorator

        Sets the decorated function as the
        entry point for the CLI app.
    '''
    global _app
    _app = func

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper

class LoggerConfig(TypedDict):
    '''
        Logger Config
    '''
    level: int
    format: str
    show_time: bool
    words_to_highlight: List[str]

@dataclass
class CliApp:
    '''
        CLI App
    '''
    name: str
    description: str
    banner: Optional[str] = ""
    name_colour: Optional[str] = "white on red"
    description_colour: Optional[str] = "white"
    banner_colour: Optional[str] = "green"
    envvars_required: Optional[List[str]] = field(default_factory=list)
    args_required: Optional[List[str]] = field(default_factory=list)
    logger_config: Optional[LoggerConfig] = None
    logger_override: Optional[logging.Logger] = None

    def __post_init__(self):
        '''
            Post Init
        '''
        if self.logger_config and self.logger_override:
            raise ValueError(
                "Cannot pass both arguments 'logger' and 'logger_override' at the same time. "
                "Either configure the built-in logger or override it. "
                "Not both."
            )

    def run(self):
        '''
            Run's the app
        '''
        if self.logger_override:
            self.logger = self.logger_override
        else:

            if not self.logger_config:
                raise ValueError(
                    "No logger config provided. "
                    "Please provide a logger config or a logger override."
                )

            # create own logger
            logger.enable_pretty_tracebacks()

            self.logger = logger.stdout(
                __name__,
                self.logger_config['level'],
                self.logger_config['format'],
                self.logger_config['show_time'],
                self.logger_config['words_to_highlight']
            )

        console = Console()
        console.print("")
        console.print(f"Welcome to {self.name}", style=self.name_colour)
        console.print(f"\n{self.description}", style=self.description_colour)

        if self.banner:
            console.print(self.banner, style=self.banner_colour)

        console.print("")

        _app(
            args.get(
                self.name,
                self.description,
                self.args_required,
                self.logger
            ),
            envvars.get(
                self.envvars_required,
                self.logger
            ),
            self.logger
        )
