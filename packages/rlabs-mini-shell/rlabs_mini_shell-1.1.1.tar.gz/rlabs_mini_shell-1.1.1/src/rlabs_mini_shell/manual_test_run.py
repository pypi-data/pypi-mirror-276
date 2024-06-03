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
    Run Manual Test
    (entry point)

    For help type:
      poetry run manual-test-run --help
'''
import logging

from rlabs_mini_shell.cmd import Cmd
from rlabs_mini_shell import logger

log = logger.stdout(
    __name__,
    logging.DEBUG
)

def main():
    '''
        main
    '''
    Cmd.date()
    Cmd.uname("-s")
    Cmd.ipconfig.getifaddr.en0()
    Cmd().ls(
        "-l",
        "tests/integration/ls_test_dir/file"
    )
    Cmd().cat(
        "tests/integration/ls_test_dir/file"
    )

    stdout, _ = Cmd().ipconfig.getifaddr.en0()
    print("My IP Address is: ", stdout)
