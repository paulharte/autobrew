from typing import List

from ..brew.brewRemote import Serializable, BrewRemote
from ..measurements.measurementSeriesRemote import MeasurementSeriesRemote


class Sync(Serializable):
    def __init__(self):
        self.brew: BrewRemote
        self.measurementSeries: List[MeasurementSeriesRemote]
