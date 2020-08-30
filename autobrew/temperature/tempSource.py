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
        return Measurement(self.get_name(), time, temp)

    def set_nickname(self, name: str):
        self.nickname = name

    def get_name(self):
        if self.nickname:
            return self.nickname
        else:
            return self._get_just_filename()

    def _get_just_filename(self):
        last_slash_index = self.device_file.rstrip("/").rfind("/")
        if last_slash_index < 0:
            return self.device_file
        second_last_slash_index = self.device_file[:last_slash_index].rstrip("/").rfind("/")
        if second_last_slash_index < 0:
            return self.device_file[last_slash_index:].strip("/")
        return self.device_file[second_last_slash_index:last_slash_index].strip("/")

    def _get_temperature(self):
        return read_temp(self.device_file)
