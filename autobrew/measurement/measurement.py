import datetime

from autobrew.aws.storage.serializable import Serializable
from autobrew.measurement.seriesType import SeriesType


class Measurement(Serializable):
    def __init__(self, source: str, time: datetime.datetime, measurement_amt: float):
        self.source_name = source
        self.time = time
        self.measurement_amt = measurement_amt

    def get_series_type(self) -> SeriesType:
        raise NotImplementedError()

    def __str__(self):
        return "%s - %s - %s" % (self.source_name, self.time, self.measurement_amt)

    def __eq__(self, other):
        return (
            (self.source_name == other.source_name)
            & (self.time == other.time)
            & (self.measurement_amt == other.measurement_amt)
        )

class TemperatureMeasurement(Measurement):
    def get_series_type(self) -> SeriesType:
        return SeriesType.TEMPERATURE


class AlcoholMeasurement(Measurement):
    def get_series_type(self) -> SeriesType:
        return SeriesType.ALCOHOL

class HeaterMeasurement(Measurement):
    def get_series_type(self) -> SeriesType:
        return SeriesType.HEATER