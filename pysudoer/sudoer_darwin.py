"""sudoer_darwin.py"""

import re
import typing
from pysudoer.sudoer_unix import SudoerUnix


class SudoerDarwin(SudoerUnix):
    """
    Run a subprocess with administrative privileges,
    prompting the user with a graphical OS dialog if necessary.
    Useful for background subprocesse which run native kivy apps that need sudo.

    * OS X, uses bundled applet (inspired by Joran Dirk Greef)

    Refactored from https://www.npmjs.com/package/@o/electron-sudo
    """

    def __init__(self, name: str, icns: str):
        _name = name if len(name.strip()) != 0 else "pysudoer-darwin"
        super().__init__(name=_name, icns=icns)

    @staticmethod
    def is_valid_name(name: str) -> bool:
        """
        check if a given string is valid by non-empty alphanumeric + space
        and less than 70 characters
        """
        foundall = re.findall(r"^[a-z0-9\s]+$", name)
        is_gt_zero = len(name.strip()) > 0
        is_lt_zero = len(name) < 70
        return any(foundall) and is_gt_zero and is_lt_zero

    def get_command(self, cmd: str) -> typing.List[str]:
        """Run AppleScript from the Command Line in Mac OS X with administrator privileges"""
        return [
            "osascript",
            "-e",
            f'"do shell script \\"{cmd}\\""',
            f'with prompt \\"{self.options.name}\\"',
            "with administrator privileges",
        ]

    def exec(self, cmd: str, env: dict[str, str], callback: typing.Callable):
        """Run a command for AppleScript"""
        cmd_escaped = re.sub(r"\"", r'\\\\\\"', cmd)
        to_exec = self.get_command(cmd_escaped)
        SudoerDarwin.run_cmd(to_exec, env=env, callback=callback)
