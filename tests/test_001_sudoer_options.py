from unittest import TestCase
from src.sudoer_options import SudoerOptions


class TestSudoerOptions(TestCase):

    def test_name(self):
        options = SudoerOptions(name="mock", icns=None)
        self.assertEqual(options.name, "mock")

    def test_icns(self):
        options = SudoerOptions(name="mock", icns="mock.icns")
        self.assertEqual(options.icns, "mock.icns")

    def test_fail_name(self):
        with self.assertRaises(ValueError) as exc_info:
            SudoerOptions(name=None, icns=None)

        self.assertEqual(str(exc_info.exception), "Name cannot be None")
