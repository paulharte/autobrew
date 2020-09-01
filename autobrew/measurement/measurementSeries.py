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
