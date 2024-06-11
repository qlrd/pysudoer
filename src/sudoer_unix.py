"""sudoer_unix.py"""

import os
import typing
import subprocess
from src.sudoer import Sudoer


class SudoerUnix(Sudoer):
    """
    Run a subprocess with administrative privileges,
    prompting the user with a graphical OS dialog if necessary.
    Useful for background subprocesse which run native kivy apps that need sudo.

    * OS X, uses bundled applet (inspired by Joran Dirk Greef)

    * Linux, uses system pkexec or gksudo (system or bundled).

    Refactored from https://www.npmjs.com/package/@o/electron-sudo
    """

    def __init__(self, name: str, icns: str):
        super().__init__(name=name if not name is None else "kivy", icns=icns)

    def copy(self, source: str, target: str, callback: typing.Callable):
        """Do a /bin/cp -R -p <source> <target>"""
        norm_source = os.path.normpath(source)
        norm_target = os.path.normpath(target)

        escaped_source = Sudoer.escape_double_quotes(norm_source)
        escaped_target = Sudoer.escape_double_quotes(norm_target)

        # pylint: disable=consider-using-with
        result = subprocess.Popen(
            ["/bin/cp", "-R", "-p", f'"{escaped_source}"', f'"{escaped_target}"'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        output, error = result.communicate()
        if error:
            raise RuntimeError(error.decode())

        callback(output.decode())

    def remove(self, target: str, callback: typing.Callable):
        """Do a /bin/rm -rf <target>"""
        print(target in self.tmp_dir)
        if not target.startswith(self.tmp_dir):
            raise ValueError(f"Try to remove suspicious target: {target}")

        norm_target = os.path.normpath(target)
        escaped_target = Sudoer.escape_double_quotes(norm_target)

        # pylint: disable=consider-using-with
        result = subprocess.Popen(
            ["/bin/rm", "-rf", f'"{escaped_target}"'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        output, error = result.communicate()
        if error:
            raise RuntimeError(error.decode())
        callback(output.decode())

    def reset(self, callback: typing.Callable):
        """Do a /usr/bin/sudo -k"""

        # pylint: disable=consider-using-with
        result = subprocess.Popen(
            [
                "/usr/bin/sudo",
                "-k",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        output, error = result.communicate()
        if error:
            raise RuntimeError(error.decode())
        callback(output.decode())
