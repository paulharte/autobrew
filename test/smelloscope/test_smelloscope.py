from unittest import TestCase

from autobrew.smelloscope.smelloscope import Smelloscope, SmelloscopeNotAvailable


class TestSmelloscope(TestCase):
    def test_exception(self):
        sm = Smelloscope()
        self.assertRaises(SmelloscopeNotAvailable, sm.get_measurement)
