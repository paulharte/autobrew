import random
from typing import List

from autobrew.temperature.tempSource import TempSource
from autobrew.temperature.tempSourceFactory import TempSourceFactory


class MockTempSourceFactory(TempSourceFactory):
    def get_temp_source(self, name: str) -> TempSource:
        return MockTempSource(name)

    def get_all_temp_sources(self) -> List[TempSource]:
        room = MockTempSource("room")
        brew = MockTempSource("brew")
        return [room, brew]


class MockTempSource(TempSource):
    def _get_temperature(self) -> float:
        ## Generates random 20 degree temp for testing
        return 20.0 + (float(random.randint(0, 9)) / 10)
