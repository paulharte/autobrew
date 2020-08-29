import datetime

from autobrew.measurement.measurement import Measurement
from autobrew.temperature.probeTempApi import read_temp


class TempSource(object):
    nickname = None
    device_file = None

    def __init__(self, device_file: str):
        self.device_file = device_file

    def get_temperature_measurement(self) -> Measurement:
        temp = self._get_temperature()
        time = datetime.datetime.now()
        return Measurement(self.device_file, time, temp)

    def set_nickname(self, name: str):
        self.nickname = name

    def get_name(self):
        return self.nickname if self.nickname else self.device_file

    def _get_temperature(self):
        return read_temp(self.device_file)
