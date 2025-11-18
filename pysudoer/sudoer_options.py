"""sudoer_options.py"""


class SudoerOptions:
    """
    SudoerOptions are simple options for define
    a properly Sudoer object

    * name: the name of the Sudoer object
    * icns: used for SudoerDarwin (macOS)
    """

    def __init__(self, name: str, icns: str | None):
        self._name = name
        self._icns = icns

    @property
    def name(self) -> str:
        """Getter for name"""
        return self._name

    @name.setter
    def name(self, value: str):
        """Setter for name"""
        self._name = value

    @property
    def icns(self) -> str | None:
        """Getter for icns"""
        return self._icns

    @icns.setter
    def icns(self, value: str | None = ""):
        """Setter for icns"""
        self._icns = value
