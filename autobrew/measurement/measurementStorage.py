from injector import inject

from autobrew.measurement.fileStorage import FileStorage
from autobrew.measurement.measurement import Measurement
from autobrew.measurement.measurementSeries import MeasurementSeries


class MeasurementStorage(object):
    """ Handles all file io for measurement series"""

    SUFFIX = ".txt"
    name: str = None

    def __init__(self, file_storage: FileStorage, name: str):
        self.name = name.replace(self.SUFFIX, "")
        self.file_storage = file_storage

    def add_measurement(self, measurement: Measurement):
        series = self.read()
        series.append(measurement)
        self._save(series)

    def set_series(self, series: MeasurementSeries):
        self._save(series)

    def read(self) -> MeasurementSeries:
        try:
            filename = self.name + self.SUFFIX
            return self.file_storage.read(filename)
        except (FileNotFoundError, EOFError):
            new_series = MeasurementSeries(self.name)
            self._save(new_series)
            return new_series

    def _save(self, series: MeasurementSeries):
        filename = self.name + self.SUFFIX
        self.file_storage.save(filename, series)
