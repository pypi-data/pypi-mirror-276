#
# Copyright (C) 2024 RomanLabs, Rafael Roman Otero
# This file is part of RLabs Mini Shell.
#
# RLabs Mini Shell is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RLabs Mini Shell is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with RLabs Mini Shell. If not, see <http://www.gnu.org/licenses/>.
#
'''
    error.py
'''
from rlabs_mini_shell import logger

log = logger.stdout(
    __name__,
    logger.logging.CRITICAL
)

class ArgumentError(TypeError):
    '''
        ArgumentError

        Raised when an argument is invalid
    '''
    def __init__(self, msg: str):

        super().__init__(msg)

class NonZeroExit(RuntimeError):
    '''
        CommandError

        Raised when a command fails
    '''
    def __init__(self,
        command: str,
        return_code: int,
        stdout: str,
        stderr: str
    ):
        if stdout:
            stdout = f"\n{stdout}"
        if stderr:
            stderr = f"\n{stderr}"

        super().__init__(
            f"Command '{command}' failed with return code {return_code}:"
            f"{stdout}"
            f"{stderr}"
        )
