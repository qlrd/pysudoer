import os
from unittest import TestCase
from unittest.mock import MagicMock, patch
from src.sudoer_unix import SudoerUnix


class TestSudoerUnix(TestCase):

    @patch("sys.platform", "linux")
    @patch("src.sudoer.subprocess.Popen")
    def test_sudoer_linux_reset(self, mock_popen):
        process_mock = MagicMock()
        attrs = {"communicate.return_value": (b"success", None)}
        process_mock.configure_mock(**attrs)
        mock_popen.return_value = process_mock

        callback = MagicMock()

        sudoer = SudoerUnix(name="mock_linux", icns=None)
        sudoer.reset(env={}, callback=callback)
        mock_popen.assert_called_once_with(
            [os.path.normpath("/usr/bin/sudo"), "-k"], env={}, stdout=-1, stderr=-1
        )

    @patch("sys.platform", "linux")
    @patch("src.sudoer.subprocess.Popen")
    def test_sudoer_linux_reset_fail(self, mock_popen):
        process_mock = MagicMock()
        attrs = {"communicate.return_value": (None, b"failed")}
        process_mock.configure_mock(**attrs)
        mock_popen.return_value = process_mock

        callback = MagicMock()

        with self.assertRaises(RuntimeError) as exc_info:
            sudoer = SudoerUnix(name="mock_linux", icns=None)
            sudoer.reset(env={}, callback=callback)

        self.assertEqual(str(exc_info.exception), "failed")
        mock_popen.assert_called_once_with(
            [os.path.normpath("/usr/bin/sudo"), "-k"], env={}, stdout=-1, stderr=-1
        )

    @patch("sys.platform", "darwin")
    @patch("src.sudoer.subprocess.Popen")
    def test_sudoer_darwin_reset(self, mock_popen):
        process_mock = MagicMock()
        attrs = {"communicate.return_value": (b"success", None)}
        process_mock.configure_mock(**attrs)
        mock_popen.return_value = process_mock

        callback = MagicMock()

        sudoer = SudoerUnix(name="mock_darwin", icns=None)
        sudoer.reset(callback=callback, env={})
        mock_popen.assert_called_once_with(
            [os.path.normpath("/usr/bin/sudo"), "-k"], env={}, stdout=-1, stderr=-1
        )

    @patch("sys.platform", "darwin")
    @patch("src.sudoer.subprocess.Popen")
    def test_sudoer_darwin_reset_fail(self, mock_popen):
        process_mock = MagicMock()
        attrs = {"communicate.return_value": (None, b"failed")}
        process_mock.configure_mock(**attrs)
        mock_popen.return_value = process_mock

        callback = MagicMock()

        with self.assertRaises(RuntimeError) as exc_info:
            sudoer = SudoerUnix(name="mock_linux", icns=None)
            sudoer.reset(env={}, callback=callback)

        self.assertEqual(str(exc_info.exception), "failed")
        mock_popen.assert_called_once_with(
            [os.path.normpath("/usr/bin/sudo"), "-k"], env={}, stdout=-1, stderr=-1
        )
