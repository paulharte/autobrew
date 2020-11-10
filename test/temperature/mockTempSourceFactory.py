import random
from typing import List

from autobrew.temperature.tempSource import TempSource
from autobrew.temperature.tempSourceFactory import TempSourceFactory

ROOM_SOURCE_NAME = "room"
BREW_SOURCE_NAME = "brew"


class MockTempSourceFactory(TempSourceFactory):
    def __init__(self):
        room = MockTempSource(ROOM_SOURCE_NAME)
        brew = MockTempSource(BREW_SOURCE_NAME)
        self.temp_sources = [room, brew]

    def get_all_temp_sources(self) -> List[TempSource]:
        return self.temp_sources


class MockTempSource(TempSource):
    def _get_temperature(self) -> float:
        ## Generates random 20 degree temp for testing
        return 20.0 + (float(random.randint(0, 9)) / 10)
