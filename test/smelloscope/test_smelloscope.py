from unittest import TestCase

from autobrew.smelloscope.smelloscope import Smelloscope, SmelloscopeNotAvailable
from test.smelloscope.stubAlcoholSensor import StubAlcoholSensor


class TestSmelloscope(TestCase):
    def test_exception(self):
        sm = Smelloscope(StubAlcoholSensor())
        self.assertEqual(type(sm.get_alcohol_level()), float)
