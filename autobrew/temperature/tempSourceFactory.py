from abc import ABC, abstractmethod
from typing import List

from injector import inject

from autobrew.temperature.probeTempApi import ProbeApi

from autobrew.temperature.tempSource import TempSource


class TempSourceFactory(ABC):

    def __init__(self):
        self.temp_sources: List[TempSource] = []

    @abstractmethod
    def get_all_temp_sources(self) -> List[TempSource]:
        pass

    def get_temp_source(self, name: str) -> TempSource:
        sources = self.get_all_temp_sources()
        for source in sources:
            if name in source.get_name():
                return source

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

    def get_primary_source(self) -> TempSource:
        for source in self.temp_sources:
            if source.is_primary:
                return source
        return None


class ProbeTempSourceFactory(TempSourceFactory):
    @inject
    def __init__(self, api: ProbeApi):
        super().__init__()
        self.api = api
        self.temp_sources = []
        self.get_all_temp_sources()

    def get_all_temp_sources(self) -> List[TempSource]:
        files = self.api.get_temp_sources()
        for file in files:
            potential_new_source = TempSource(self.api, file)
            if potential_new_source not in self.temp_sources:
                self.temp_sources.append(potential_new_source)
        return self.temp_sources
