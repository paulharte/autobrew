from autobrew.brew_settings import SMELLOSCOPE_OFFSET


class StubAlcoholSensor(object):

    def __init__(self):
        self._i = 0

    def setupMcp(self):
        pass

    def get_voltage(self) -> float:
        # Voltage will decrease over time, simulating increasing alcohol
        self._i += 1
        return SMELLOSCOPE_OFFSET - (self._i / 100)
