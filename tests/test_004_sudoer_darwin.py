from unittest import mock

from pysudoer.sudoer_darwin import SudoerDarwin

# pylint: disable=unused-import
from .shared import mock_darwin


# pylint: disable=unused-argument,redefined-outer-name
def test_init(mock_darwin):
    sudoer = SudoerDarwin(name="mock_darwin", icns="mock.icns")
    assert sudoer.options.name == "mock_darwin"
    assert sudoer.options.icns == "mock.icns"
    assert sudoer.platform == "darwin"


# pylint: disable=unused-argument,redefined-outer-name
def test_is_valid_name_alphanumeric_less_than_70(mock_darwin):
    cases = ["mock1234", "mock 1234", "mockdarwin"]

    n = 0
    for case in cases:
        print(f"Case {n}: {cases[n]}")
        is_valid = SudoerDarwin.is_valid_name(case)
        assert is_valid
        n += 1


# pylint: disable=unused-argument,redefined-outer-name
def test_get_command(mock_darwin):
    sudoer = SudoerDarwin(name="mock_darwin", icns="mock.icns")
    command = sudoer.get_command("echo 'mock'")
    result = [
        "osascript",
        "-e",
        '"do shell script \\"echo \'mock\'\\""',
        f'with prompt \\"{sudoer.options.name}\\"',
        "with administrator privileges",
    ]
    assert command == result


# pylint: disable=unused-argument,redefined-outer-name
def test_exec(mock_darwin):
    sudoer = SudoerDarwin(name="mock_darwin", icns="mock.icns")
    callback = mock.MagicMock()

    with mock.patch.object(SudoerDarwin, "run_cmd") as run_cmd:
        sudoer.exec("echo 'mock'", env={}, callback=callback)

        expected_cmd = [
            "osascript",
            "-e",
            '"do shell script \\"echo \'mock\'\\""',
            'with prompt \\"mock_darwin\\"',
            "with administrator privileges",
        ]
        run_cmd.assert_called_once_with(expected_cmd, env={}, callback=callback)
