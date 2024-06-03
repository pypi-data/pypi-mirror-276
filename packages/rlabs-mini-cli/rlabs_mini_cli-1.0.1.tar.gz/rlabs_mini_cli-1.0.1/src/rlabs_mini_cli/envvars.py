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
    cli.py
'''
import os
import logging

from rlabs_mini_cli import error

class EnvVars:
        def __str__(self) -> str:
            '''
                Returns a string representation of the object

                Returns a comma separated string of
                all envvars as they would be accessed

                e.g.
                    my_var, my_other_var
            '''
            envvars = []
            for attribute in vars(self):
                envvars.append(
                    f"EnvVar({attribute}={getattr(self, attribute)})"
                )

            return ", ".join(envvars)

def get(
        envvars_required: list[str],
        logger: logging.Logger
    ) -> EnvVars:
    '''
        Collects required envvars. Returns them as attributes
        of an EnvVars object with the same name in lowercase.

        e.g.
            MY_VAR is returned as my_var

        Raises error.MissingEnvVar if an envvar is missing
    '''
    _envvars = EnvVars()

    for envvar_name in envvars_required:

        try:
            setattr(
                _envvars,
                envvar_name.lower(),
                os.environ[envvar_name]
            )

        except KeyError:
            raise error.MissingEnvVar(
                envvar_name
            ) from None

    logger.debug(f"Found CLI envvars: {[key.upper() for key in vars(_envvars).keys()]}")

    return _envvars


