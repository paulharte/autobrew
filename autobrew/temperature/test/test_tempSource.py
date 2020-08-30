from unittest import TestCase

from autobrew.temperature.tempSource import TempSource


class TestTempSource(TestCase):
    def test_name(self):
        source = TempSource("filename")
        self.assertEqual(source.get_name(), "filename")
        source.set_nickname("nick")
        self.assertEqual(source.get_name(), "nick")

        source2 = TempSource("path/to/a/filename2")
        self.assertEqual(source2.get_name(), "filename2")

        source3 = TempSource("path/to/a/filename3/")
        self.assertEqual(source3.get_name(), "filename3")
