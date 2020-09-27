from abc import ABC, abstractmethod
from typing import List

from autobrew.temperature.probeTempApi import get_temp_sources

from autobrew.temperature.tempSource import TempSource


class TempSourceFactory(ABC):
    temp_sources: List[TempSource]
    @abstractmethod
    def get_temp_source(self, name: str) -> TempSource:
        pass

    @abstractmethod
    def get_all_temp_sources(self) -> List[TempSource]:
        pass

    def remove_temp_source(self, to_remove: TempSource):
        self.temp_sources.remove(to_remove)

    def set_primary_source(self, name: str) -> bool:
        success = False
        for i in range(len(self.temp_sources)):
            if self.temp_sources[i].get_name() == name:
                self.temp_sources[i].set_primary(True)
                success = True
            else:
                self.temp_sources[i].set_primary(False)

        return success


class ProbeTempSourceFactory(TempSourceFactory):

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

