from unittest import TestCase
from unittest.mock import MagicMock, patch
from src.sudoer_unix import SudoerUnix


class TestSudoerLinux(TestCase):

    @patch("sys.platform", "linux")
    @patch("src.sudoer.subprocess.Popen")
    def test_sudoer_linux_copy(self, mock_popen):
        process_mock = MagicMock()
        attrs = {"communicate.return_value": (b"success", None)}
        process_mock.configure_mock(**attrs)
        mock_popen.return_value = process_mock

        callback = MagicMock()

        sudoer = SudoerUnix(name="mock_linux", icns=None)
        sudoer.copy("/tmp/mock.txt", "/tmp/test.txt", callback=callback)
        mock_popen.assert_called_once_with(
            ["/bin/cp", "-R", "-p", '"/tmp/mock.txt"', '"/tmp/test.txt"'],
            stdout=-1,
            stderr=-1,
        )
        callback.assert_called_once_with("success")

    @patch("sys.platform", "linux")
    @patch("src.sudoer.subprocess.Popen")
    def test_sudoer_linux_copy_fail(self, mock_popen):
        process_mock = MagicMock()
        attrs = {"communicate.return_value": (None, b"error")}
        process_mock.configure_mock(**attrs)
        mock_popen.return_value = process_mock

        callback = MagicMock()

        sudoer = SudoerUnix(name="mock_linux", icns=None)

        with self.assertRaises(RuntimeError) as exc_info:
            sudoer.copy("/tmp/mock.txt", "/tmp/test.txt", callback=callback)

        self.assertEqual(str(exc_info.exception), "error")
        mock_popen.assert_called_once_with(
            ["/bin/cp", "-R", "-p", '"/tmp/mock.txt"', '"/tmp/test.txt"'],
            stdout=-1,
            stderr=-1,
        )

    @patch("sys.platform", "linux")
    @patch("src.sudoer.tempfile.mkdtemp", lambda: "/tmp")
    @patch("src.sudoer.subprocess.Popen")
    def test_sudoer_linux_remove(self, mock_popen):
        process_mock = MagicMock()
        attrs = {"communicate.return_value": (b"success", None)}
        process_mock.configure_mock(**attrs)
        mock_popen.return_value = process_mock

        callback = MagicMock()

        sudoer = SudoerUnix(name="mock_linux", icns=None)
        sudoer.remove("/tmp/mock.txt", callback=callback)
        mock_popen.assert_called_once_with(
            ["/bin/rm", "-rf", '"/tmp/mock.txt"'], stdout=-1, stderr=-1
        )
        callback.assert_called_once_with("success")

    @patch("sys.platform", "linux")
    @patch("src.sudoer.tempfile.mkdtemp", lambda: "/tmp")
    def test_sudoer_linux_remove_fail_target(self):
        callback = MagicMock()

        with self.assertRaises(ValueError) as exc_info:
            sudoer = SudoerUnix(name="mock_linux", icns=None)
            sudoer.remove("/usr/mock.txt", callback=callback)

        self.assertEqual(
            str(exc_info.exception), "Try to remove suspicious target: /usr/mock.txt"
        )

    @patch("sys.platform", "linux")
    @patch("src.sudoer.tempfile.mkdtemp", lambda: "/tmp")
    @patch("src.sudoer.subprocess.Popen")
    def test_sudoer_linux_remove_fail(self, mock_popen):
        process_mock = MagicMock()
        attrs = {"communicate.return_value": (None, b"error")}
        process_mock.configure_mock(**attrs)
        mock_popen.return_value = process_mock

        callback = MagicMock()

        sudoer = SudoerUnix(name="mock_linux", icns=None)

        with self.assertRaises(RuntimeError) as exc_info:
            sudoer.remove("/tmp/mock.txt", callback=callback)

        self.assertEqual(str(exc_info.exception), "error")
        mock_popen.assert_called_once_with(
            ["/bin/rm", "-rf", '"/tmp/mock.txt"'], stdout=-1, stderr=-1
        )

    @patch("sys.platform", "linux")
    @patch("src.sudoer.subprocess.Popen")
    def test_sudoer_linux_reset(self, mock_popen):
        process_mock = MagicMock()
        attrs = {"communicate.return_value": (b"success", None)}
        process_mock.configure_mock(**attrs)
        mock_popen.return_value = process_mock

        callback = MagicMock()

        sudoer = SudoerUnix(name="mock_linux", icns=None)
        sudoer.reset(callback=callback)
        mock_popen.assert_called_once_with(
            ["/usr/bin/sudo", "-k"], stdout=-1, stderr=-1
        )

    @patch("sys.platform", "darwin")
    @patch("src.sudoer.subprocess.Popen")
    def test_sudoer_darwin_copy(self, mock_popen):
        process_mock = MagicMock()
        attrs = {"communicate.return_value": (b"success", None)}
        process_mock.configure_mock(**attrs)
        mock_popen.return_value = process_mock

        callback = MagicMock()

        sudoer = SudoerUnix(name="mock_darwin", icns=None)
        sudoer.copy("/tmp/mock.txt", "/tmp/test.txt", callback=callback)
        mock_popen.assert_called_once_with(
            ["/bin/cp", "-R", "-p", '"/tmp/mock.txt"', '"/tmp/test.txt"'],
            stdout=-1,
            stderr=-1,
        )
        callback.assert_called_once_with("success")

    @patch("sys.platform", "darwin")
    @patch("src.sudoer.subprocess.Popen")
    def test_sudoer_darwin_copy_fail(self, mock_popen):
        process_mock = MagicMock()
        attrs = {"communicate.return_value": (None, b"error")}
        process_mock.configure_mock(**attrs)
        mock_popen.return_value = process_mock

        callback = MagicMock()

        sudoer = SudoerUnix(name="mock_darwin", icns=None)

        with self.assertRaises(RuntimeError) as exc_info:
            sudoer.copy("/tmp/mock.txt", "/tmp/test.txt", callback=callback)

        self.assertEqual(str(exc_info.exception), "error")
        mock_popen.assert_called_once_with(
            ["/bin/cp", "-R", "-p", '"/tmp/mock.txt"', '"/tmp/test.txt"'],
            stdout=-1,
            stderr=-1,
        )

    @patch("sys.platform", "darwin")
    @patch("src.sudoer.tempfile.mkdtemp", lambda: "/tmp")
    @patch("src.sudoer.subprocess.Popen")
    def test_sudoer_darwin_remove(self, mock_popen):
        process_mock = MagicMock()
        attrs = {"communicate.return_value": (b"success", None)}
        process_mock.configure_mock(**attrs)
        mock_popen.return_value = process_mock

        callback = MagicMock()

        sudoer = SudoerUnix(name="mock_darwin", icns=None)
        sudoer.remove("/tmp/mock.txt", callback=callback)
        mock_popen.assert_called_once_with(
            ["/bin/rm", "-rf", '"/tmp/mock.txt"'], stdout=-1, stderr=-1
        )
        callback.assert_called_once_with("success")

    @patch("sys.platform", "darwin")
    @patch("src.sudoer.tempfile.mkdtemp", lambda: "/tmp")
    def test_sudoer_darwin_remove_fail_target(self):
        callback = MagicMock()

        with self.assertRaises(ValueError) as exc_info:
            sudoer = SudoerUnix(name="mock_darwin", icns=None)
            sudoer.remove("/usr/mock.txt", callback=callback)

        self.assertEqual(
            str(exc_info.exception), "Try to remove suspicious target: /usr/mock.txt"
        )

    @patch("sys.platform", "darwin")
    @patch("src.sudoer.tempfile.mkdtemp", lambda: "/tmp")
    @patch("src.sudoer.subprocess.Popen")
    def test_sudoer_darwin_remove_fail(self, mock_popen):
        process_mock = MagicMock()
        attrs = {"communicate.return_value": (None, b"error")}
        process_mock.configure_mock(**attrs)
        mock_popen.return_value = process_mock

        callback = MagicMock()

        sudoer = SudoerUnix(name="mock_darwin", icns=None)

        with self.assertRaises(RuntimeError) as exc_info:
            sudoer.remove("/tmp/mock.txt", callback=callback)

        self.assertEqual(str(exc_info.exception), "error")
        mock_popen.assert_called_once_with(
            ["/bin/rm", "-rf", '"/tmp/mock.txt"'], stdout=-1, stderr=-1
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
        sudoer.reset(callback=callback)
        mock_popen.assert_called_once_with(
            ["/usr/bin/sudo", "-k"], stdout=-1, stderr=-1
        )
