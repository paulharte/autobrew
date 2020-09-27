from abc import ABC, abstractmethod
from typing import List

from autobrew.temperature.probeTempApi import get_temp_sources

from autobrew.temperature.tempSource import TempSource


class TempSourceFactory(ABC):
    @abstractmethod
    def get_temp_source(self, name: str) -> TempSource:
        pass

    @abstractmethod
    def get_all_temp_sources(self) -> List[TempSource]:
        pass


class ProbeTempSourceFactory(TempSourceFactory):
    temp_sources: List[TempSource]

    def __init__(self):
        self.temp_sources = []

    def get_temp_source(self, name: str) -> TempSource:
        sources = self.get_all_temp_sources()
        for source in sources:
            if name in source.get_name():
                return source

    def get_all_temp_sources(self) -> List[TempSource]:
        files = get_temp_sources()
        for file in files:
            potential_new_source = TempSource(file)
            if potential_new_source not in self.temp_sources:
                self.temp_sources.append(potential_new_source)
        return self.temp_sources

    def remove_temp_source(self, to_remove: TempSource):
        self.temp_sources.remove(to_remove)
