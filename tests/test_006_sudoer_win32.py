import os
from unittest import TestCase
from unittest.mock import MagicMock, patch, call, mock_open
from pysudoer.sudoer_win32 import SudoerWin32


class TestSudoerWin32(TestCase):
    @patch("sys.platform", "win32")
    def test_init(self):
        sudoer = SudoerWin32(name="mock_win")
        self.assertEqual(sudoer.options.name, "mock_win")
        self.assertEqual(sudoer.options.icns, None)

    @patch("sys.platform", "win32")
    def test_bundled(self):
        dir_name = os.path.dirname(__file__)
        bin_path = os.path.join(dir_name, "..", "pysudoer", "bin")
        elevate = os.path.normpath(os.path.join(bin_path, "elevate.exe"))

        sudoer = SudoerWin32(name="mock_win")
        self.assertEqual(sudoer.bundled, elevate)

    @patch("sys.platform", "win32")
    @patch("pysudoer.sudoer.tempfile.mkdtemp", return_value="C:\\TEMP\\mock")
    @patch("pysudoer.sudoer_win32.random.randrange", side_effect=[12345, 6789])
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

    # pylint: disable=too-many-positional-arguments
    @patch("sys.platform", "win32")
    @patch("pysudoer.sudoer.tempfile.mkdtemp", return_value="C:\\TEMP\\mock")
    @patch("pysudoer.sudoer_win32.random.randrange", side_effect=[12345, 6789])
    @patch("builtins.open", new_callable=mock_open())
    @patch("pysudoer.sudoer_win32.os.path.exists", side_effect=[False])
    @patch("pysudoer.sudoer_win32.shutil.copyfile")
    @patch("pysudoer.sudoer.subprocess.Popen")
    def test_exec(
        self,
        mock_popen,
        mock_copyfile,
        mock_exists,
        open_mock,
        mock_randrange,
        mock_mkdtemp,
    ):
        process_mock = MagicMock()
        attrs = {"communicate.return_value": (b"success", None)}
        process_mock.configure_mock(**attrs)
        mock_popen.return_value = process_mock

        dir_name = os.path.dirname(__file__)
        bin_path = os.path.join(dir_name, "..", "pysudoer", "bin")
        elevate_path = os.path.normpath(os.path.join(bin_path, "elevate.exe"))

        callback = MagicMock()
        sudoer = SudoerWin32(name="mock_win")
        sudoer.exec(cmd=["echo", "'Hello World'"], env={}, callback=callback)
        mock_mkdtemp.assert_called_once()
        mock_randrange.assert_has_calls([call(10000), call(10000)])

        # pylint: disable=unnecessary-dunder-call
        open_mock.assert_has_calls(
            [
                call("C:\\TEMP\\mock\\batch-12345.bat", "w", encoding="utf8"),
                call().__enter__(),
                call()
                .__enter__()
                .write(
                    "setlocal enabledelayedexpansion\r\necho 'Hello World' > C:\\TEMP\\mock\\output-6789"
                ),
                call().__exit__(None, None, None),
                call("C:\\TEMP\\mock\\output-6789", "w", encoding="utf8"),
                call().__enter__(),
                call().__enter__().write(""),
                call().__exit__(None, None, None),
            ]
        )
        mock_exists.assert_called_once_with(
            "C:\\TEMP\\mock" + os.path.normpath("/elevate.exe")
        )
        mock_copyfile.assert_called_once_with(
            elevate_path, "C:\\TEMP\\mock" + os.path.normpath("/elevate.exe")
        )
        mock_popen.assert_called_once_with(
            [
                '"C:\\TEMP\\mock' + os.path.normpath("/elevate.exe") + '"',
                "-wait",
                "C:\\TEMP\\mock\\batch-12345.bat",
            ],
            env={},
            stderr=-1,
            stdout=-1,
        )
