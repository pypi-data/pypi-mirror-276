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
import logging
import argparse

from rlabs_mini_cli import cli
from rlabs_mini_cli import envvars

myapp_banner = r"""
  __  __
 |  \/  |         /\
 | \  / |_   _   /  \   _ __  _ __
 | |\/| | | | | / /\ \ | '_ \| '_ \
 | |  | | |_| |/ ____ \| |_) | |_) |
 |_|  |_|\__, /_/    \_\ .__/| .__/
          __/ |        | |   | |
         |___/         |_|   |_|
"""

@cli.app
def myapp(
    args: argparse.Namespace,
    envs: envvars.EnvVars,
    logger: logging.Logger
):
    '''
        CLI App
    '''
    logger.info("Hey there, this is MyApp")
    logger.info(f"args: {args}")
    logger.info(f"envvars: {envs}")

    logger.info(f"envvar1: {envs.var1}")
    logger.info(f"env_var2: {envs.var2}")
    logger.info(f"arg1: {args.arg1}")
    logger.info(f"arg_2: {args.arg_2}")
    logger.info(f"arg-3: {args.arg_3}")

def main():
    '''
        main
    '''
    myapp = cli.CliApp(
        name="MyApp",
        description="MyApp is an amazing CLIApp",
        banner=myapp_banner,
        name_colour="white on red",
        banner_colour="green",
        description_colour="white",
        envvars_required=[
            "VAR1",
            "VAR2"
        ],
        args_required=[
            "arg1",
            "arg_2",
            "arg-3"
        ],
        logger_config={
            "level": logging.DEBUG,
            "format": "%(message)s",
            "show_time": False,
            "words_to_highlight": [
                "hello",
                "there"
            ]
        }
    )
    myapp.run()
