from autobrew.measurement.measurement import Measurement
from typing import List


class MeasurementSeries(object):
    measurements: List[Measurement]
    name: str
    nickname: str = None

    def __init__(self, name: str):
        self.name = name.replace(self.SUFFIX, "")
        self.measurements = []
