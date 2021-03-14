from autobrew.measurement.measurement import Measurement
from typing import List


class MeasurementSeries(object):
    def __init__(self, source_name: str, brew_id: int):
        self.source_name: str = source_name
        self.measurements: List[Measurement] = []
        self.brew_id: int = brew_id
        self.nickname: str = None

    @property
    def id(self) -> str:
        return str(self.brew_id) + self.source_name

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
