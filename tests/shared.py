from unittest import mock

import pytest
from pysudoer import sudoer


@pytest.fixture
def mock_linux(monkeypatch):
    sys_mod = mock.MagicMock(platform="linux")
    monkeypatch.setattr(sudoer, "sys", sys_mod)


@pytest.fixture
def mock_win32(monkeypatch):
    sys_mod = mock.MagicMock(platform="win32")
    monkeypatch.setattr(sudoer, "sys", sys_mod)


@pytest.fixture
def mock_darwin(monkeypatch):
    sys_mod = mock.MagicMock(platform="darwin")
    monkeypatch.setattr(sudoer, "sys", sys_mod)


@pytest.fixture
def mock_bytes():
    with mock.patch("pysudoer.sudoer.io.BytesIO") as bytesio_cls:
        io_bytes_mock = mock.MagicMock()
        attrs = {"getbuffer.return_value": {"nbytes": 0}, "getvalue.return_value": ""}
        io_bytes_mock.configure_mock(**attrs)
        bytesio_cls.return_value = io_bytes_mock
        yield io_bytes_mock
