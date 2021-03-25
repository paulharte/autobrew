from typing import List

from injector import inject

from autobrew.brew.brew import Brew

from autobrew.measurement.measurement import Measurement
from autobrew.measurement.measurementSeries import MeasurementSeries
from autobrew.measurement.measurementStorage import MeasurementStorage


class MeasurementService(object):
    @inject
    def __init__(self, storage: MeasurementStorage):
        self.storage = storage

    def save_measurement(
        self, measurement: Measurement, brew: Brew
    ) -> MeasurementSeries:
        series = self.storage.read_by_source(measurement.source_name, brew.id)
        if not series:
            series = self.new_series(brew, measurement.source_name)
        series.append(measurement)
        self.save_series(series)
        return series

    def new_series(self, brew: Brew, source_name: str) -> MeasurementSeries:
        series = MeasurementSeries(source_name, brew.id)
        self.storage.save(series)
        return series

    def get_all_series_for_brew(self, brew: Brew) -> List[MeasurementSeries]:
        all_series = self.storage.get_all_series()
        measurements = []
        for series in all_series:
            if series.brew_id == brew.id:
                measurements.append(series)
        return measurements

    def get_series(self, series_id: str) -> MeasurementSeries:
        return self.storage.read(series_id)

    def get_series_by_source(self, source_name: str, brew_id: str) -> MeasurementSeries:
        return self.storage.read_by_source(source_name, brew_id)

    def set_measurement_nickname(
        self, series_id: str, nickname: str
    ) -> MeasurementSeries:
        for series in self.storage.get_all_series():
            if series.id == series_id:
                series.nickname = nickname
                self.save_series(series)
                return series

    def save_series(self, series: MeasurementSeries) -> MeasurementSeries:
        self.storage.save(series)
        return series
