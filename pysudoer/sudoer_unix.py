"""sudoer_unix.py"""

import typing
from pysudoer.sudoer import Sudoer


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
        super().__init__(name=name, icns=icns)

    def reset(self, env: typing.Dict[str, str], callback: typing.Callable):
        """Invalidate the timestamp file (sudo -k)"""
        SudoerUnix.run_cmd(["/usr/bin/sudo", "-k"], env=env, callback=callback)
