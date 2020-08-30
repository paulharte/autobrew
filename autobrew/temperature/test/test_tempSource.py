from unittest import TestCase

from autobrew.temperature.tempSource import TempSource


class TestTempSource(TestCase):
    def test_nickname(self):
        source = TempSource("filename")
        self.assertEqual(source.get_name(), "filename")
        source.set_nickname("nick")
        self.assertEqual(source.get_name(), "nick")
    
    def test_filename(self):
        source2 = TempSource("path/to/a/filename2")
        self.assertEqual(source2.get_name(), "a")

        source3 = TempSource("/sys/bus/w1/devices/uniquename/w1_slave")
        self.assertEqual(source3.get_name(), "uniquename")
        
        source4 = TempSource("sys/bus/w1/devices/28-041651652cff/w1_slave")
        self.assertEqual(source4.get_name(), "28-041651652cff")
        
