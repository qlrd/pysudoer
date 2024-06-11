import os
from unittest import TestCase
from unittest.mock import MagicMock, patch, call
from src.sudoer_linux import SudoerLinux


class TestSudoerLinux(TestCase):

    @patch("sys.platform", "linux")
    def test_init(self):
        sudoer = SudoerLinux(name="mock_linux")
        self.assertEqual(sudoer.options.name, "mock_linux")
        self.assertEqual(sudoer.options.icns, None)

    @patch("sys.platform", "linux")
    def test_get_paths(self):
        binaries = SudoerLinux.get_paths()
        self.assertEqual(binaries[0], "/usr/bin/gksudo")
        self.assertEqual(binaries[1], "/usr/bin/pkexec")

    @patch("sys.platform", "linux")
    @patch("src.sudoer_linux.os.path.exists", side_effect=[True])
    def test_get_binary_usr_bin_gksudo(self, mock_exists):
        binary = SudoerLinux.get_binary()
        mock_exists.assert_has_calls([call("/usr/bin/gksudo")])
        self.assertEqual(binary, "/usr/bin/gksudo")

    @patch("sys.platform", "linux")
    @patch("src.sudoer_linux.os.path.exists", side_effect=[False, True])
    def test_get_binary_usr_bin_pkexec(self, mock_exists):
        binary = SudoerLinux.get_binary()
        mock_exists.assert_has_calls([call("/usr/bin/gksudo"), call("/usr/bin/pkexec")])
        self.assertEqual(binary, "/usr/bin/pkexec")

    @patch("sys.platform", "linux")
    @patch("src.sudoer_linux.os.path.exists", side_effect=[False, False, True])
    def test_get_binary_local_gksudo(self, mock_exists):
        binary = SudoerLinux.get_binary()

        dir_name = os.path.dirname(__file__)
        bin_path = os.path.join(dir_name, "..", "bin")
        local_bin = os.path.normpath(os.path.join(bin_path, "gksudo"))

        mock_exists.assert_has_calls(
            [call("/usr/bin/gksudo"), call("/usr/bin/pkexec"), call(local_bin)]
        )
        self.assertEqual(binary, local_bin)

    @patch("sys.platform", "linux")
    @patch("src.sudoer_linux.os.path.exists", side_effect=[True])
    @patch("src.sudoer_linux.os.environ.copy", return_value={"USER": "mock"})
    @patch("src.sudoer.subprocess.Popen")
    def test_exec_with_usr_bin_gksudo(self, mock_popen, mock_copy, mock_exists):
        process_mock = MagicMock()
        attrs = {"communicate.return_value": (b"success", None)}
        process_mock.configure_mock(**attrs)
        mock_popen.return_value = process_mock

        sudoer = SudoerLinux(name="mock_linux")
        callback = MagicMock()

        sudoer.exec(cmd=["echo", "-v", "'mock'"], env=None, callback=callback)
        mock_exists.assert_called_once_with("/usr/bin/gksudo")
        mock_copy.assert_called_once()
        mock_popen.assert_called_once_with(
            [
                "/usr/bin/gksudo",
                "--preserve-env",
                "--sudo-mode",
                "--description=mock_linux",
                "echo",
                "-v",
                "'mock'",
            ],
            env={"USER": "mock", "DISPLAY": ":0"},
            stdout=-1,
            stderr=-1,
        )

    @patch("sys.platform", "linux")
    @patch("src.sudoer_linux.os.path.exists", side_effect=[False, True])
    @patch("src.sudoer_linux.os.environ.copy", return_value={"USER": "mock"})
    @patch("src.sudoer.subprocess.Popen")
    def test_exec_with_usr_bin_pkexec(self, mock_popen, mock_copy, mock_exists):
        process_mock = MagicMock()
        attrs = {"communicate.return_value": (b"success", None)}
        process_mock.configure_mock(**attrs)
        mock_popen.return_value = process_mock

        sudoer = SudoerLinux(name="mock_linux")
        callback = MagicMock()

        sudoer.exec(cmd=["echo", "-v", "'mock'"], env=None, callback=callback)
        mock_exists.assert_has_calls([call("/usr/bin/gksudo"), call("/usr/bin/pkexec")])
        mock_copy.assert_called_once()
        mock_popen.assert_called_once_with(
            ["/usr/bin/pkexec", "--disable-internal-agent", "echo", "-v", "'mock'"],
            env={"USER": "mock", "DISPLAY": ":0"},
            stdout=-1,
            stderr=-1,
        )
