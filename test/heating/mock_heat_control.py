from autobrew.heating.heat_control import HeatControl


class MockHeatControl(HeatControl):
    def _switch_power(self, on: bool):
        pass
