import time

from autobrew.temperature.probeTempApi import ProbeApi

""" This is a useful script for testing the DS18B20 temperature probes attached to your raspberry pi.
Will work for x number of attached probes (you can attach them to the same pins)
A good tutorial on how to hook up a single on and install is here: pimylifeup.com/raspberry-pi-temperature-sensor/
"""


def run():
    probe_api = ProbeApi()
    device_files = probe_api.get_temp_sources()
    while True:
        for file in device_files:
            print("File: " + str(file))
            print(probe_api.read_temp(file))
        time.sleep(2)


if __name__ == "__main__":
    run()
