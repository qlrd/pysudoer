from pysudoer.sudoer import Sudoer, SudoerOptions

# pylint: disable=unused-import
from .shared import mock_bytes, mock_linux, mock_darwin, mock_win32


# pylint: disable=unused-argument,redefined-outer-name
def test_sudoer_linux(mock_linux):
    sudoer = Sudoer(name="mock")
    assert sudoer.options.name == "mock"
    assert sudoer.platform == "linux"

    options = SudoerOptions(name="test", icns=None)
    sudoer.options = options
    assert sudoer.options.name != "mock"


# pylint: disable=unused-argument,redefined-outer-name
def test_sudoer_windows(mock_win32):
    sudoer = Sudoer(name="mock")
    assert sudoer.options.name == "mock"
    assert sudoer.platform == "win32"


# pylint: disable=unused-argument,redefined-outer-name
def test_sudoer_darwin(mock_darwin):
    sudoer = Sudoer(name="mock")
    assert sudoer.options.name == "mock"
    assert sudoer.platform == "darwin"


# pylint: disable=unused-argument,redefined-outer-name
def test_hash(mock_bytes):
    sudoer = Sudoer(name="mock")
    h = sudoer.hash()
    assert h == "32125346b1ddddcd768ef44c1d109dfa"


def test_join_env():
    env = Sudoer.join_env({"TEST": "mock", "MOCK": "test"})
    assert env == ["TEST=mock", "MOCK=test"]


def test_escape_double_quotes():
    msg = Sudoer.escape_double_quotes('"mock message"')
    assert msg == '\\"mock message\\"'


def test_enclose_double_quotes():
    msg = Sudoer.enclose_double_quotes("mock message")
    assert msg == '"mock message"'
