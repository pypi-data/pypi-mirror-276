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
    Cmd
'''
import logging
import subprocess
from typing import ClassVar

from rlabs_mini_shell.error import ArgumentError, NonZeroExit
from rlabs_mini_shell import logger

class CmdMeta(type):
    def __getattr__(cls, method_name: str):
        '''
            __getattr__

            Captures get attribute calls
            to the Cmd class

            This enables the chaining of commands
            STARTING FROM Cmd, as opposed to Cmd()

            e.g.

                Cmd.i.am.a.command.withh.arguments("arg1")

        '''
        return Cmd(method_name)

class Cmd(metaclass=CmdMeta):
    _log: ClassVar[logging.Logger] = logger.stdout(__name__, logging.DEBUG)
    __is_first_call: ClassVar[bool] = False

    @classmethod
    def log_setup(cls, log_level: int):
        '''
            log_setup

            Sets up logging for all commands
        '''
        Cmd._log = logger.stdout(__name__, log_level)

    def __init__(self, cmd_str_to_add=''):
        '''
            __init__
        '''
        if not Cmd.__is_first_call:
            # enable pretty tracebacks
            logger.enable_pretty_tracebacks()
            Cmd.__is_first_call = True

        self.cmd_str = cmd_str_to_add

    def __getattr__(self, method_name: str):
        '''
            __getattr__

            Captures get attribute calls

            Returns a new Cmd object with
            the attribute name appended to cmd_str
        '''
        if self.cmd_str:
            return Cmd(f"{self.cmd_str} {method_name}")
        else:
            #
            # this runs only once
            # when the first method is called
            #
            # e.g.
            #   Cmd().i.am.a.command.withh.arguments("arg1")
            #
            #   calling i will return a new Cmd object
            #   with cmd_str set to i
            #
            #   Therefore, the next call to am will append to cmd_str
            #   and so forth
            #
            return Cmd(method_name)

    def __call__(self, *args, **kwargs):
        '''
            __call__

            Captures call to object

            This is the last call in the chain
            and will execute the command with
            the arguments passed in
        '''
        if kwargs:
            raise ArgumentError(
                f"Shell Command object cannot take keyword arguments"
            )
        return self.__execute_command(
            self.__add_args(self.cmd_str, *args)
        )

    def __add_args(self, cmd_str: str, *args) -> str:
        '''
            Add arguments to command string

            Returns a string with the command string
            and arguments appended to it

            e.g.

                In:

                Cmd().i.am.a.command.withh.arguments("arg1")

                cmd_str = "i am a command withh arguments"
                args = ("arg1",)

                will return:
                    "i am a command withh arguments arg1"
        '''
        args_str = ' '.join(str(arg) for arg in args)
        return f"{cmd_str} {args_str}"

    def __execute_command(self, cmd_str: str) -> tuple[str, str]:
        '''
            Execute command in cmd_str
        '''
        Cmd._log.debug(cmd_str)

        output = subprocess.run(
            cmd_str,
            capture_output=True,
            shell=True, # There's more to this but the main
                        # reason is that shell=False will
                        # raise exceptions on non-zero exit codes
            text=True,
            check=False # Don't raise exception on non-zero exit code
        )

        if output.stdout:
            Cmd._log.info(output.stdout)

        if output.stderr:
            Cmd._log.error(output.stderr)

        if output.returncode != 0:
            raise NonZeroExit(
                cmd_str,
                output.returncode,
                output.stdout,
                output.stderr
            )

        stdout = output.stdout.strip() if output.stdout else ''
        stderr = output.stderr.strip() if output.stderr else ''

        return stdout, stderr

