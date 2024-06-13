"""sudoer_linux.py"""

import os
import typing
import random
import shutil
import tempfile
from src.sudoer import Sudoer


class SudoerWin32(Sudoer):
    """
    Run a subprocess with administrative privileges,
    prompting the user with a graphical OS dialog if necessary.
    Useful for background subprocesse which run native kivy apps that need sudo.

    * Windows, uses elevate utility with native User Account Control
      (UAC) prompt (no PowerShell required)

    Refactored from https://www.npmjs.com/package/@o/electron-sudo
    """

    def __init__(self, name: str):
        super().__init__(name=name, icns=None)
        self.binary = None

    @property
    def bundled(self) -> str:
        """Return the path of bundled elevate.exe"""
        dir_name = os.path.dirname(__file__)
        bin_path = os.path.join(dir_name, "bin")
        return os.path.normpath(os.path.join(bin_path, "elevate.exe"))

    def write_batch(self, cmd: typing.List[str], env: typing.Dict[str, str]):
        """Write a batch file"""
        tmp_batch_file = os.path.normpath(
            f"{self.tmp_dir}\\batch-{random.randrange(10000)}.bat"
        )
        tmp_output_file = os.path.normpath(
            f"{self.tmp_dir}\\output-{random.randrange(10000)}"
        )

        batch = ["setlocal enabledelayedexpansion"]

        if len(env.keys()) > 0:
            for key, val in env.items():
                batch.append(f"set {key}={val}")

        batch.append(" ".join(cmd))
        print(batch)
        batch_txt = "\r\n".join(batch)

        with open(tmp_batch_file, "w", encoding="utf8") as batch_file:
            batch_file.write(f"{batch_txt} > {tmp_output_file}")

        with open(tmp_output_file, "w", encoding="utf8") as output_file:
            output_file.write("")

        return (tmp_batch_file, tmp_output_file)

    def exec(
        self, cmd: typing.List[str], env=typing.Dict[str, str], callback=typing.Callable
    ):
        """Execute a command with elevate.exe"""
        if not self.binary:
            try:
                # Copy applet to temporary directory
                target = os.path.join(self.tmp_dir, "elevate.exe")
                target = os.path.normpath(target)

                if not os.path.exists(target):
                    shutil.copyfile(self.bundled, target)
                    self.binary = target
                else:
                    raise FileExistsError(f"'{target}' already exist")

            except PermissionError as p_exc:
                raise RuntimeError(p_exc) from p_exc
            except shutil.SameFileError as sf_exc:
                raise RuntimeError(sf_exc) from sf_exc
            except IOError as io_exc:
                raise RuntimeError(io_exc) from io_exc

        files = self.write_batch(cmd=cmd, env=env)
        enclosed_binary = self.enclose_double_quotes(self.binary)
        command = [enclosed_binary, "-wait", files[0]]
        SudoerWin32.run_cmd(cmd=command, env=env, callback=callback)
