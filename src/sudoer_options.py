"""sudoer_options.py"""
import re
import typing


class SudoerOptions:
    """
    SudoerOptions are simple options for define
    a properly Sudoer object

    * name: the name of the Sudoer object
    * icns: used for SudoerDarwin (macOS)
    """
    def __init__(self, name: str, icns: str):
        self.name = name
        self.icns = icns

    @property
    def name(self) -> str:
        """Getter for name"""
        return self._name

    @name.setter
    def name(self, value: str):
        """Setter for name"""
        if not value is None:
            self._name = value
        else:
            raise ValueError("Name cannot be None")

    @property
    def icns(self) -> str:
        """Getter for icns"""
        return self._icns

    @icns.setter
    def icns(self, value: str = ""):
        """Setter for icns"""
        if value is None:
            self._icns = ""  
        elif re.findall(r"^.*\.icns$", value):
            self._icns = value
        else:
            raise ValueError(f"Invalid icns: {value}")
