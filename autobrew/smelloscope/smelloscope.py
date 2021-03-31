import datetime

from injector import inject

from autobrew.brew_settings import SMELLOSCOPE_OFFSET
from autobrew.measurement.measurement import AlcoholMeasurement
from autobrew.smelloscope.hardware_alcohol_sensor import HardwareAlcoholSensor
from autobrew.temperature.abstractSource import AbstractSource


class Smelloscope(AbstractSource):

    NAME = "Alcohol_Smelloscope"
    mcp = None

    @inject
    def __init__(self, alcohol_sensor: HardwareAlcoholSensor):
        super()
        self.alcohol_sensor = alcohol_sensor
        self.is_primary = True

    def get_name(self):
        return self.NAME

    def _get_voltage(self) -> float:
        try:
            return self.alcohol_sensor.get_voltage()
        except Exception as e:
            raise SmelloscopeNotAvailable(e)

    def get_alcohol_level(self) -> float:
        return SMELLOSCOPE_OFFSET - self._get_voltage()

    def get_measurement(self) -> AlcoholMeasurement:
        time = datetime.datetime.utcnow()
        alcohol_level = self.get_alcohol_level()
        measurement = AlcoholMeasurement(self.NAME, time, alcohol_level)
        return measurement

    def __eq__(self, other):
        return self.get_name() == other.get_name()


class SmelloscopeNotAvailable(RuntimeError):
    pass
