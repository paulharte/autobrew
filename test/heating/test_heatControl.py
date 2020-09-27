from unittest import TestCase, mock
import autobrew.heating.heat_control as heat_control


class TestHeatControl(TestCase):
    def test_adjust(self):
        mock_api = mock.Mock()
        heat_control.switch_power = mock_api
        heat_control.MAX_TEMP_C = 30.0
        heat_control.MIN_TEMP_C = 20.0
        control = heat_control.HeatControl()
        control.adjust(100.00)
        self.assertFalse(control._power_is_on)
        control.adjust(25.00)
        self.assertFalse(control._power_is_on)
        control.adjust(-100.00)
        self.assertTrue(control._power_is_on)
        control.adjust(25.00)
        self.assertTrue(control._power_is_on)
