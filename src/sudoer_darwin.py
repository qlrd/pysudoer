"""sudoer_darwin.py"""

import re
import typing
from src.sudoer_unix import SudoerUnix


class SudoerDarwin(SudoerUnix):
    """
    Run a subprocess with administrative privileges,
    prompting the user with a graphical OS dialog if necessary.
    Useful for background subprocesse which run native kivy apps that need sudo.

    * OS X, uses bundled applet (inspired by Joran Dirk Greef)

    Refactored from https://www.npmjs.com/package/@o/electron-sudo
    """

    def __init__(self, name: str, icns: str):
        super().__init__(name=name if not name is None else "kivy", icns=icns)
        if icns is None:
            raise ValueError("icns must be a string if provided")
        if len(icns.strip()) == 0:
            raise ValueError("icns must be a non-empty string if provided")

    @staticmethod
    def is_valid_name(name: str) -> bool:
        """
        check if a given string is valid by non-empty alphanumeric + space
        and less than 70 characters
        """
        return (
            re.findall(r"^[a-z0-9\s]+$", name)
            and len(name.strip()) > 0
            and len(name) < 70
        )

    def get_command(self, cmd: str) -> typing.List[str]:
        """Run AppleScript from the Command Line in Mac OS X with administrator privileges"""
        return [
            "osascript -e",
            f'"do shell script \\"{cmd}\\"',
            f'with prompt \\"{self.options.name}\\"',
            "with administrator privileges",
        ]

    def exec(self, cmd: str, env: typing.Callable, callback: typing.Callable):
        """Run a command for AppleScript"""
        cmd_escaped = re.sub(r"\"", r'\\\\\\"', cmd)
        to_exec = self.get_command(cmd_escaped)
        SudoerDarwin.run_cmd(to_exec, env=env, callback=callback)
