from autobrew.temperature.tempSource import TempSource
from autobrew.utils.temperature_probe_tester import get_temp_sources


def get_temp_source(name: str) -> TempSource:
    files = get_temp_sources()
    for file in files:
        if name in file:
            return TempSource(file)
