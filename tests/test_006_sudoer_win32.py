import os
from unittest import TestCase
from unittest.mock import patch, call, mock_open
from src.sudoer_win32 import SudoerWin32


class TestSudoerLinux(TestCase):

    @patch("sys.platform", "win32")
    def test_init(self):
        sudoer = SudoerWin32(name="mock_win")
        self.assertEqual(sudoer.options.name, "mock_win")
        self.assertEqual(sudoer.options.icns, None)

    @patch("sys.platform", "win32")
    def test_bundled(self):
        dir_name = os.path.dirname(__file__)
        bin_path = os.path.join(dir_name, "..", "src", "bin")
        elevate = os.path.normpath(os.path.join(bin_path, "elevate.exe"))

        sudoer = SudoerWin32(name="mock_win")
        self.assertEqual(sudoer.bundled, elevate)

    @patch("sys.platform", "win32")
    @patch("src.sudoer_win32.tempfile.mkdtemp", return_value="C:\\TEMP\\mock")
    @patch("src.sudoer_win32.random.randrange", side_effect=[12345, 6789])
    @patch("builtins.open", new_callable=mock_open())
    def test_write_batch(self, open_mock, mock_randrange, mock_mkdtemp):
        sudoer = SudoerWin32(name="mock_win")
        result = sudoer.write_batch(cmd=["echo", "'Hello world'"], env={})

        mock_mkdtemp.assert_called_once()
        mock_randrange.assert_has_calls([call(10000), call(10000)])

        writed_file = "\r\n".join(
            [
                "setlocal enabledelayedexpansion",
                "echo 'Hello world' > C:\\TEMP\\mock\\output-6789",
            ]
        )

        open_mock.assert_has_calls(
            [
                call("C:\\TEMP\\mock\\batch-12345.bat", "w", encoding="utf8"),
                # pylint: disable=unnecessary-dunder-call
                call().__enter__(),
                # pylint: disable=unnecessary-dunder-call
                call().__enter__().write(writed_file),
                # pylint: disable=unnecessary-dunder-call
                call().__exit__(None, None, None),
                call("C:\\TEMP\\mock\\output-6789", "w", encoding="utf8"),
                # pylint: disable=unnecessary-dunder-call
                call().__enter__(),
                # pylint: disable=unnecessary-dunder-call
                call().__enter__().write(""),
                # pylint: disable=unnecessary-dunder-call
                call().__exit__(None, None, None),
            ]
        )

        self.assertEqual(result[0], "C:\\TEMP\\mock\\batch-12345.bat")
        self.assertEqual(result[1], "C:\\TEMP\\mock\\output-6789")
