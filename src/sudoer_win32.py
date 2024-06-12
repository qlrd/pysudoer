"""sudoer_linux.py"""

import os
import typing
import randomi
import shutil
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
        this.bundled = "\\src\\bin\\elevate.exe"
        this.binary = None

    @property
    def bundled(self) -> str:
        return "\\src\\bin\\elevate.exe"

    def write_batch(self, cmd: typing.List[str], env: typing.Dict[str, str]):
        tmp_dir = tempfile.gettempdir()
        tmp_batch_file = f"{tmp_dir}\\batch-{random.randrange(10000)}.bat"
        tmp_output_file = f"{tmp_dir}\\output-${random.randrange(10000)}"

        batch = ["setlocal enabledelayedexpansion", "set"]        
        if len(env.keys()) > 0:
            batch.append(f"set {'\r\nset '.join(env}")

        for c in cmd:
            batch.append(c)

        batch = "\r\n".join(batch)

        print(batch)

        with open(tmp_batch_file, "w", encoding="utf8") as batch_file:
            batch_file.write(f"{btach} > {tmp_output_file}")

        with open(tmp_output_file, "w", encoding="utf8") as output_file:
            output_file.write("")

        return (tmp_batch_file, tmp_output_file)

    def prepare(self):
        if self.binary:
            pass
        else:
            try:
                tmp_dir = tempfile.gettempdir()
            
                # Copy applet to temporary directory
                target = os.path.join(tmp_dir, 'elevate.exe')
                target = os.path.normpath(target)

                if not os.path.exists(target):
                    shutil.copyfile(self.bundled, target)
                    self.binary = target
                else:
                    raise FileExistsError(f"'{target}' already exist")
                    
            except IOError as io_exc:
                raise RuntimeError(io_exc.message)
            except PermissionError as p_exc:
                raise RuntimeError(p_exc.message)
            except SameFileError as sf_exc:
                raise RuntimeError(sf.message)
            else:
                raise Exception("Unknow error")
    
    def exec(self, cmd: typing.List[str], env=typing.Dict[str, str], callback=typing.Callable):
        result = self.prepare()
        if result:
            files = self.write_batch(cmd=cmd, env=env)
            enclosed_binary = self.encolse_double_quotes(self.binary)
            command = [ enclosed_binary, "-wait", files[0] ]
            SudoerWini32.run_cmd(cmd=cmd, env=os.environ.copy(), callback=callback)
        else:
            raise result
