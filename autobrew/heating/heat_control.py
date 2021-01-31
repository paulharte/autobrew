from injector import inject

from autobrew.brew_settings import MIN_TEMP_C, MAX_TEMP_C
from autobrew.heating.heat_switcher import HeatSwitcher


class HeatControl(object):
    _power_is_on: bool

    @inject
    def __init__(self, heat_switcher: HeatSwitcher):
        self.heat_switcher = heat_switcher
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
        # Assume on is default state for external purposes
        return self._power_is_on in [None, True]

    def _switch_power(self, on: bool):
        self.heat_switcher.switch(on)
