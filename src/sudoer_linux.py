"""sudoer_linux.py"""

import os
import typing
from src.sudoer_unix import SudoerUnix


class SudoerLinux(SudoerUnix):
    """
    Run a subprocess with administrative privileges,
    prompting the user with a graphical OS dialog if necessary.
    Useful for background subprocesse which run native kivy apps that need sudo.

    * Linux, uses system pkexec or gksudo (system or bundled).

    Refactored from https://www.npmjs.com/package/@o/electron-sudo
    """

    def __init__(self, name: str):
        super().__init__(name=name, icns=None)

    @staticmethod
    def get_binary() -> str:
        """Getter for binary"""
        binary = None
        for _bin in SudoerLinux.get_paths():
            if os.path.exists(_bin):
                binary = _bin
                break

        if binary is None:
            raise RuntimeError("Any polkit executable found")

        return binary

    @staticmethod
    def get_paths() -> typing.List[str]:
        """Return a list of possible paths por polkit binaries"""
        dir_name = os.path.dirname(__file__)
        bin_path = os.path.join(dir_name, "..", "bin")
        local_bin = os.path.normpath(os.path.join(bin_path, "gksudo"))
        return ["/usr/bin/gksudo", "/usr/bin/pkexec", local_bin]

    def exec(
        self,
        cmd: typing.List[str],
        env: typing.Dict[str, str],
        callback: typing.Callable,
    ):
        """Execute a pkexec | gksudo with own environ"""
        if not env:
            env = os.environ.copy()

        if not "DISPLAY" in env.keys():
            env["DISPLAY"] = ":0"

        binary = SudoerLinux.get_binary()
        flags = []

        if "gksudo" in binary:
            escaped_name = self.escape_double_quotes(self.options.name)
            flags = ["--preserve-env", "--sudo-mode", f"--description={escaped_name}"]

        elif "pkexec" in binary:
            flags = ["--disable-internal-agent"]

        result = []
        result.append(binary)

        for f in flags:
            result.append(f)

        for c in cmd:
            result.append(c)

        SudoerLinux.run_cmd(result, env=env, callback=callback)
