from unittest import TestCase
from unittest.mock import MagicMock, patch
from src.sudoer_options import SudoerOptions
from src.sudoer import Sudoer

class TestSudoer(TestCase):

    @patch("sys.platform", "linux")
    @patch("src.sudoer.subprocess.Popen")
    def test_sudoer_linux(self, mock_popen):
        process_mock = MagicMock()
        attrs = {"communicate.return_value": ("output", "success")}
        process_mock.configure_mock(**attrs)
        mock_popen.return_value = process_mock
        
        sudoer = Sudoer(
            name="mock",
            child_process=mock_popen
        )
        mock_popen.communicate()
        self.assertEqual(sudoer.options.name, "mock")
        self.assertEqual(sudoer.platform, "linux")
        mock_popen.communicate.assert_called_once()
    
    @patch("sys.platform", "win32")
    @patch("src.sudoer.subprocess.Popen")
    def test_sudoer_windows(self, mock_popen):
        process_mock = MagicMock()
        attrs = {"communicate.return_value": ("output", "success")}
        process_mock.configure_mock(**attrs)
        mock_popen.return_value = process_mock
        
        sudoer = Sudoer(
            name="mock",
            child_process=mock_popen
        )
        mock_popen.communicate()
        self.assertEqual(sudoer.options.name, "mock")
        self.assertEqual(sudoer.platform, "win32")
        mock_popen.communicate.assert_called_once()
        
    @patch("sys.platform", "darwin")
    @patch("src.sudoer.subprocess.Popen")
    def test_sudoer_darwin(self, mock_popen):
        process_mock = MagicMock()
        attrs = {"communicate.return_value": ("output", "success")}
        process_mock.configure_mock(**attrs)
        mock_popen.return_value = process_mock
        
        sudoer = Sudoer(
            name="mock",
            child_process=mock_popen
        )
        mock_popen.communicate()
        self.assertEqual(sudoer.options.name, "mock")
        self.assertEqual(sudoer.platform, "darwin")
        mock_popen.communicate.assert_called_once()

    
    @patch("src.sudoer.subprocess.Popen")
    @patch("src.sudoer.io.BytesIO")
    def test_hash(self, mock_io, mock_popen):
        process_mock = MagicMock()
        attrs = {"communicate.return_value": ("output", "success")}
        process_mock.configure_mock(**attrs)
        mock_popen.return_value = process_mock

        io_bytes_mock = MagicMock()
        attrs = {
            "getbuffer.return_value": {"nbytes": 0},
            "getvalue.return_value": ""
        }
        io_bytes_mock.configure_mock(**attrs)
        mock_io.return_value = io_bytes_mock
        
        sudoer = Sudoer(
            name="mock",
            child_process=mock_popen
        )
        h = sudoer.hash()
        self.assertEqual(h, "32125346b1ddddcd768ef44c1d109dfa")

    def test_join_env(self):
        env = Sudoer.join_env({ "TEST": "mock", "MOCK": "test"})
        self.assertEqual(env, ["TEST=mock", "MOCK=test"])

    
    def test_escape_double_quotes(self):
        msg = Sudoer.escape_double_quotes("\"mock message\"")
        self.assertEqual(msg, "\\\"mock message\\\"")
    
    def test_enclose_double_quotes(self):
        msg = Sudoer.enclose_double_quotes("mock message")
        self.assertEqual(msg, "\"mock message\"")

    @patch("src.sudoer.Sudoer.kill")
    def test_kill(self, mock_kill):
        Sudoer.kill(1234)
        mock_kill.assert_called_once_with(1234)
        
        
