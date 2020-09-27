from autobrew.measurement.measurement import Measurement
from typing import List


class MeasurementSeries(object):
    measurements: List[Measurement]
    source_name: str
    nickname: str = None

    def __init__(self, source_name: str):
        self.source_name = source_name
        self.measurements = []

    def append(self, measurement: Measurement):
        self.measurements.append(measurement)

    def get_name(self):
        return self.nickname if self.nickname else self.source_name

    def get_measurements(self) -> List[Measurement]:
        self.measurements.sort(key=lambda x: x.time)
        return self.measurements

    def get_max_amount(self) -> float:
        best_measurement_amt = None
        for measurement in self.measurements:
            if (best_measurement_amt is None) or (
                measurement.measurement_amt > best_measurement_amt
            ):
                best_measurement_amt = measurement.measurement_amt
        return best_measurement_amt

    def get_min_amount(self) -> float:
        best_measurement_amt = None
        for measurement in self.measurements:
            if (best_measurement_amt is None) or (
                measurement.measurement_amt < best_measurement_amt
            ):
                best_measurement_amt = measurement.measurement_amt
        return best_measurement_amt
