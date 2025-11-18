import os
import sys
from unittest import mock

import pytest
from pysudoer.sudoer_unix import SudoerUnix

# pylint: disable=unused-import
from .shared import mock_linux


# pylint: disable=unused-argument,redefined-outer-name
def test_sudoer_unix_reset(mocker, mock_linux):
    if sys.platform != "win32":
        run_cmd = mocker.patch("pysudoer.sudoer_unix.SudoerUnix.run_cmd")
        callback = mock.MagicMock(return_value=True)
        su = SudoerUnix(name="mockunix", icns=None)
        su.reset(env={}, callback=callback)
        run_cmd.assert_called_once_with(
            [os.path.normpath("/usr/bin/sudo"), "-k"], env={}, callback=callback
        )


# pylint: disable=unused-argument,redefined-outer-name
def test_sudoer_unix_reset_fail(mocker, mock_linux):
    if sys.platform != "win32":
        callback = mock.MagicMock()
        communicate = mocker.patch(
            "pysudoer.sudoer.subprocess.Popen.communicate",
            return_value=(None, b"failed"),
        )

        with pytest.raises(RuntimeError, match="failed"):
            su = SudoerUnix(name="mockunix", icns=None)
            su.reset(env={}, callback=callback)

        communicate.assert_called_once()
