from typing import List

from injector import inject

from autobrew.smelloscope.hardware_alcohol_sensor import HardwareAlcoholSensor
from autobrew.smelloscope.smelloscope import Smelloscope


class SmelloscopeFactory(object):
    @inject
    def __init__(self, alcohol_sensor: HardwareAlcoholSensor):
        self.sensor = alcohol_sensor
        self.sources = []
        self.get_all_sources()

    def get_all_sources(self) -> List[Smelloscope]:
        self.sources = [Smelloscope(self.sensor)]
        return self.sources

    def get_source(self, source_name: str) -> Smelloscope:
        sources = self.get_all_sources()
        for source in sources:
            if source_name in source.get_name():
                return source

    def remove_source(self, to_remove: Smelloscope):
        self.sources.remove(to_remove)
