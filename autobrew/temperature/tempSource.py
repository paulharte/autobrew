import datetime

from autobrew.measurement.measurement import Measurement
from autobrew.temperature.abstractSource import AbstractSource
from autobrew.temperature.probeTempApi import ProbeApi

PROBE_PREFIX = "Probe_"
RETRY_MAX_AMOUNT = 50.0
RETRY_MIN_AMOUNT = 0.0


class TempSource(AbstractSource):
    def __init__(self, api: ProbeApi, device_file: str):
        super()
        self.device_file = device_file
        self.api = api

    def __eq__(self, other):
        return self.get_name() == other.get_name()

    def get_name(self):
        return PROBE_PREFIX + self._get_just_filename()

    def get_temperature_measurement(self) -> Measurement:
        temp = self._get_temperature()
        time = datetime.datetime.utcnow()
        return Measurement(self.get_name(), time, temp)

    def _get_just_filename(self):
        last_slash_index = self.device_file.rstrip("/").rfind("/")
        if last_slash_index < 0:
            return self.device_file
        second_last_slash_index = (
            self.device_file[:last_slash_index].rstrip("/").rfind("/")
        )
        if second_last_slash_index < 0:
            return self.device_file[last_slash_index:].strip("/")
        return self.device_file[second_last_slash_index:last_slash_index].strip("/")

    def _get_temperature(self) -> float:
        temp = self.api.read_temp(self.device_file)
        # Retry if we get an extreme value back
        if (temp > RETRY_MAX_AMOUNT) | (temp < RETRY_MIN_AMOUNT):
            return self.api.read_temp(self.device_file)
        return temp
