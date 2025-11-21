from pysudoer.sudoer_options import SudoerOptions


def test_name():
    options = SudoerOptions(name="mock", icns=None)
    assert options.name == "mock"

    options.name = "test"
    assert options.name != "mock"


def test_icns():
    options = SudoerOptions(name="mock", icns="mock.icns")
    assert options.icns == "mock.icns"

    options.icns = "test.icns"
    assert options.icns != "mock.icns"
