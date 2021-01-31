from unittest import TestCase, mock
import autobrew.heating.heat_control as heat_control
from test.heating.mock_heat_control import MockHeatSwitcher


class TestHeatControl(TestCase):
    def test_adjust(self):
        heat_control.MAX_TEMP_C = 30.0
        heat_control.MIN_TEMP_C = 20.0
        control = heat_control.HeatControl(MockHeatSwitcher())
        control.adjust(100.00)
        self.assertFalse(control._power_is_on)
        control.adjust(25.00)
        self.assertFalse(control._power_is_on)
        control.adjust(-100.00)
        self.assertTrue(control._power_is_on)
        control.adjust(25.00)
        self.assertTrue(control._power_is_on)
