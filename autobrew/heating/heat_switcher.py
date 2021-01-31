from autobrew.heating.usb_api import switch_power


class HeatSwitcher(object):
    def switch(self, on: bool):
        return switch_power(on)
