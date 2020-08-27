import os
from typing import List

from autobrew.measurement.measurementSeries import MeasurementSeries
from autobrew.measurement.storage import MeasurementStorage


class MeasurementService(object):
    def get_all_series(self) -> List[MeasurementSeries]:
        filenames = self._get_files()
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

    def _get_files(self) -> List[str]:
        files = os.listdir()
        return filter(lambda x: x.endswith(MeasurementStorage.SUFFIX), files)

    def save_series(self, series: MeasurementSeries) -> MeasurementSeries:
        filenames = self._get_files()
        for filename in filenames:
            storage = MeasurementStorage(filename)
            if storage.name == series.name:
                storage.set_series(series)
                return series
