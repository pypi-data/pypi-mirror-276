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
    error.py
'''

class NoAppDefined(RuntimeError):
    '''
        NoAppDefined

        Raised when no app is defined
    '''
    def __init__(self):
        super().__init__(
            "No App defined. Please use the @app decorator "
            "on a function that will be your CLI app's entry point."
        )

class MissingEnvVar(RuntimeError):
    '''
        MissingEnvVar

        Raised when a required envvar is missing
    '''
    def __init__(self, envvar: str):
        super().__init__(
            f"Missing required envvar: {envvar}. "
        )
