from typing import List

from autobrew.measurement.measurement import Measurement
from autobrew.measurement.measurementSeries import MeasurementSeries
from autobrew.measurement.measurementStorage import MeasurementStorage, get_storage_files


class MeasurementService(object):
    def save_measurement(self, measurement: Measurement):
        MeasurementStorage(measurement.source_name).add_measurement(measurement)

    def get_all_series(self) -> List[MeasurementSeries]:
        filenames = get_storage_files()
        measurements = []
        for filename in filenames:
            measurements.append(MeasurementStorage(filename).read())
        return measurements

    def set_measurement_nickname(self, name: str, nickname: str) -> MeasurementSeries:
        for series in self.get_all_series():
            if series.name == name:
                series.nickname = nickname
                self.save_series(series)
                return series

    def save_series(self, series: MeasurementSeries) -> MeasurementSeries:
        filenames = get_storage_files()
        for filename in filenames:
            storage = MeasurementStorage(filename)
            if storage.name == series.name:
                storage.set_series(series)
                return series
