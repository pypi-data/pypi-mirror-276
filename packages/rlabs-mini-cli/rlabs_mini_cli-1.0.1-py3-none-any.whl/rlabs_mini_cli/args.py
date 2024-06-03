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
    Args
'''
import argparse
import logging

def get(
        app_name: str,
        app_description: str,
        args_required: list[str],
        logger: logging.Logger
    ) -> argparse.Namespace:
    '''
        Returns a parsed namespace from the CLI arguments
        provided when running the application.
    '''
    parser = argparse.ArgumentParser(
        prog=app_name,
        description=app_description
    )

    # required args
    for required in args_required:
        parser.add_argument(
            f"--{required}",
            required=True
        )

    parsed_args = parser.parse_args()

    logger.debug(f"Found CLI args: {vars(parsed_args)}")

    return parsed_args
