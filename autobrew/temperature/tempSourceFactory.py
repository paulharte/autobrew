from typing import List

from autobrew.temperature.probeTempApi import (
    get_temp_sources,
    initialise_probes,
    read_temp,
)
from autobrew.temperature.tempSource import TempSource

from abc import ABC, abstractmethod


class TempSourceFactory(ABC):
    @abstractmethod
    def get_temp_source(self, name: str) -> TempSource:
        pass

    @abstractmethod
    def get_all_temp_sources(self) -> List[TempSource]:
        pass


class ProbeTempSourceFactory(TempSourceFactory):
    def get_temp_source(self, name: str) -> TempSource:
        sources = self.get_all_temp_sources()
        for source in sources:
            if name in source.device_file:
                return source

    def get_all_temp_sources(self) -> List[TempSource]:
        files = get_temp_sources()
        out = []
        for file in files:
            out.append(TempSource(file))
        return out
