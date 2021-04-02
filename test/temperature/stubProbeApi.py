import random

from autobrew.temperature.probeTempApi import InvalidTemperatureFileError

STUB_BREW_TEMP_NAME = "brew"
STUB_ROOM_TEMP_NAME = "room"


class StubProbeApi(object):
    def __init__(self):
        pass

    def initialise_probes(self):
        pass

    def get_temp_sources(self) -> []:
        return [STUB_BREW_TEMP_NAME, STUB_ROOM_TEMP_NAME]

    def read_temp(self, file: str) -> float:
        if file not in self.get_temp_sources():
            raise InvalidTemperatureFileError(file)
        # Generates random 20 degree temp for testing
        return 20.0 + (float(random.randint(0, 9)) / 10)
