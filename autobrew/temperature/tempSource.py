from autobrew.utils.temperature_probe_tester import read_temp, initialise_probes


class TempSource(object):
    nickname = None
    device_file = None

    def __init__(self, device_file: str):
        self.device_file = device_file
        initialise_probes()

    def get_temperature(self) -> float:
        return read_temp(self.device_file)


