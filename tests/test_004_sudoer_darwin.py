from unittest import TestCase
from unittest.mock import MagicMock, patch
from src.sudoer_darwin import SudoerDarwin


class TestSudoerDarwin(TestCase):

    @patch("sys.platform", "darwin")
    def test_init(self):
        sudoer = SudoerDarwin(name="mock_darwin", icns="mock.icns")
        self.assertEqual(sudoer.options.name, "mock_darwin")
        self.assertEqual(sudoer.options.icns, "mock.icns")

    @patch("sys.platform", "darwin")
    def test_fail_init_not_provided(self):
        with self.assertRaises(ValueError) as exc_info:
            SudoerDarwin(name="mock_darwin", icns=None)

        self.assertEqual(str(exc_info.exception), "icns must be a string if provided")

    @patch("sys.platform", "darwin")
    def test_fail_init_empty_string(self):
        with self.assertRaises(ValueError) as exc_info:
            SudoerDarwin(name="mock_darwin", icns="")

        self.assertEqual(
            str(exc_info.exception), "icns must be a non-empty string if provided"
        )

    def test_is_valid_name_alphanumeric_less_than_70(self):
        is_valid = SudoerDarwin.is_valid_name("mock1234")
        self.assertTrue(is_valid)

    def test_is_valid_name_alphanumeric_less_than_70_with_space(self):
        is_valid = SudoerDarwin.is_valid_name("mock 1234")
        self.assertTrue(is_valid)

    def test_isnt_valid_name_no_alphanumeric(self):
        is_valid = SudoerDarwin.is_valid_name("mock+")
        self.assertFalse(is_valid)

    def test_isnt_valid_name_empty(self):
        is_valid = SudoerDarwin.is_valid_name("")
        self.assertFalse(is_valid)

    def test_isnt_valid_greater_than_70(self):
        is_valid = SudoerDarwin.is_valid_name(
            "qwertyuiopasdfghjkl134567890zxcvbnm0987654321asdfghjklpoiuytrewqzxcvbnm"
        )
        self.assertFalse(is_valid)

    def test_get_command(self):
        sudoer = SudoerDarwin(name="mock_darwin", icns="mock.icns")
        command = sudoer.get_command("echo 'mock'")
        self.assertEqual(
            command,
            [
                "osascript -e",
                '"do shell script \\"echo \'mock\'\\"',
                'with prompt \\"mock_darwin\\"',
                "with administrator privileges",
            ],
        )

    @patch("sys.platform", "darwin")
    @patch("src.sudoer.subprocess.Popen")
    def test_exec(self, mock_popen):
        process_mock = MagicMock()
        attrs = {"communicate.return_value": (b"success", None)}
        process_mock.configure_mock(**attrs)
        mock_popen.return_value = process_mock

        callback = MagicMock()

        sudoer = SudoerDarwin(name="mock_darwin", icns="mock.icns")
        sudoer.exec("echo 'mock'", env={}, callback=callback)
        mock_popen.assert_called_once_with(
            [
                "osascript -e",
                '"do shell script \\"echo \'mock\'\\"',
                'with prompt \\"mock_darwin\\"',
                "with administrator privileges",
            ],
            env={},
            stdout=-1,
            stderr=-1,
        )
