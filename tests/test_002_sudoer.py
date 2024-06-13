from unittest import TestCase
from unittest.mock import MagicMock, patch
from pysudoer.sudoer import Sudoer


class TestSudoer(TestCase):

    @patch("sys.platform", "linux")
    def test_sudoer_linux(self):
        sudoer = Sudoer(name="mock")
        self.assertEqual(sudoer.options.name, "mock")
        self.assertEqual(sudoer.platform, "linux")

    @patch("sys.platform", "win32")
    def test_sudoer_windows(self):
        sudoer = Sudoer(name="mock")
        self.assertEqual(sudoer.options.name, "mock")
        self.assertEqual(sudoer.platform, "win32")

    @patch("sys.platform", "darwin")
    def test_sudoer_darwin(self):
        sudoer = Sudoer(name="mock")
        self.assertEqual(sudoer.options.name, "mock")
        self.assertEqual(sudoer.platform, "darwin")

    @patch("pysudoer.sudoer.io.BytesIO")
    def test_hash(self, mock_io):
        io_bytes_mock = MagicMock()
        attrs = {"getbuffer.return_value": {"nbytes": 0}, "getvalue.return_value": ""}
        io_bytes_mock.configure_mock(**attrs)
        mock_io.return_value = io_bytes_mock

        sudoer = Sudoer(name="mock")
        h = sudoer.hash()
        self.assertEqual(h, "32125346b1ddddcd768ef44c1d109dfa")

    def test_join_env(self):
        env = Sudoer.join_env({"TEST": "mock", "MOCK": "test"})
        self.assertEqual(env, ["TEST=mock", "MOCK=test"])

    def test_escape_double_quotes(self):
        msg = Sudoer.escape_double_quotes('"mock message"')
        self.assertEqual(msg, '\\"mock message\\"')

    def test_enclose_double_quotes(self):
        msg = Sudoer.enclose_double_quotes("mock message")
        self.assertEqual(msg, '"mock message"')

    @patch("pysudoer.sudoer.Sudoer.kill")
    def test_kill(self, mock_kill):
        Sudoer.kill(1234)
        mock_kill.assert_called_once_with(1234)
