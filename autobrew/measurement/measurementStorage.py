import os
import pickle
from typing import List

from autobrew.measurement.measurement import Measurement
from autobrew.measurement.measurementSeries import MeasurementSeries

FOLDER_NAME = "storage"
FOLDER_PATH = os.path.dirname(os.path.abspath(__file__)).replace(
    "measurement", FOLDER_NAME
)


def get_storage_files() -> List[str]:
    files = os.listdir(FOLDER_PATH)
    return filter(lambda x: x.endswith(MeasurementStorage.SUFFIX), files)


class MeasurementStorage(object):
    """ Handles all file io for measurement series"""

    SUFFIX = ".txt"
    name: str = None

    def __init__(self, name: str):
        self.name = name.replace(self.SUFFIX, "")

    def add_measurement(self, measurement: Measurement):
        series = self.read()
        series.append(measurement)
        self._save(series)

    def set_series(self, series: MeasurementSeries):
        self._save(series)

    def read(self) -> MeasurementSeries:
        try:
            with open(FOLDER_PATH + "/" + self.name + self.SUFFIX, "rb") as file:
                data = pickle.load(file)
        except (FileNotFoundError, EOFError):
            new_series = MeasurementSeries(self.name)
            self._save(new_series)
            return new_series
        return data

    def _save(self, series: MeasurementSeries):
        with open(FOLDER_PATH + "/" + self.name + self.SUFFIX, "wb") as file:
            pickle.dump(series, file)
