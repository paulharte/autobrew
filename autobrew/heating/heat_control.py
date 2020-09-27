from autobrew.brew_settings import MIN_TEMP_C, MAX_TEMP_C
from autobrew.heating.usb_api import switch_power


class HeatControl(object):
    _power_is_on: bool

    def __init__(self):
        self._power_is_on = None  # We don't know state on startup
        if MIN_TEMP_C > MAX_TEMP_C:
            raise RuntimeError("MIN_TEMP_C cannot be higher than MAX_TEMP_C")

    def adjust(self, current_temperature: float):
        if current_temperature < MIN_TEMP_C:
            self.turn_on()
        elif current_temperature > MAX_TEMP_C:
            self.turn_off()

    def turn_on(self):
        if self._power_is_on in [None, False]:
            self._switch_power(True)
            self._power_is_on = True

    def turn_off(self):
        if self._power_is_on in [None, True]:
            self._switch_power(False)
            self._power_is_on = False

    def is_power_on(self):
        return self._power_is_on

    def _switch_power(self, on: bool):
        switch_power(on)
