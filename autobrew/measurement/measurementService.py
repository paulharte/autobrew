from typing import List

from injector import inject

from autobrew.measurement.fileStorage import FileStorage
from autobrew.measurement.measurement import Measurement
from autobrew.measurement.measurementSeries import MeasurementSeries
from autobrew.measurement.measurementStorage import MeasurementStorage


class MeasurementService(object):
    @inject
    def __init__(self, file_storage: FileStorage):
        self.file_storage = file_storage

    def save_measurement(self, measurement: Measurement):
        MeasurementStorage(self.file_storage, measurement.source_name).add_measurement(
            measurement
        )

    def get_all_series(self) -> List[MeasurementSeries]:
        filenames = self.file_storage.get_storage_files()
        measurements = []
        for filename in filenames:
            measurements.append(MeasurementStorage(self.file_storage, filename).read())
        return measurements

    def get_series(self, name) -> MeasurementSeries:
        filenames = self.file_storage.get_storage_files()
        for filename in filenames:
            storage = MeasurementStorage(self.file_storage, filename)
            if storage.name == name:
                return storage.read()

    def set_measurement_nickname(self, name: str, nickname: str) -> MeasurementSeries:
        for series in self.get_all_series():
            if series.name == name:
                series.nickname = nickname
                self.save_series(series)
                return series

    def save_series(self, series: MeasurementSeries) -> MeasurementSeries:
        filenames = self.file_storage.get_storage_files()
        for filename in filenames:
            storage = MeasurementStorage(self.file_storage, filename)
            if storage.name == series.get_name():
                storage.set_series(series)
                return series
