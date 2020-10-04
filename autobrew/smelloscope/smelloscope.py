import datetime

import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as mcp3008
from adafruit_mcp3xxx.analog_in import AnalogIn

from autobrew.brew_settings import SMELLOSCOPE_OFFSET
from autobrew.measurement.measurement import Measurement


class Smelloscope(object):

    NAME = "Alcohol_Smelloscope"

    def __init__(self):
        # create the spi bus
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

        # create the cs (chip select)
        cs = digitalio.DigitalInOut(board.D5)

        # create the mcp object
        self.mcp = mcp3008.MCP3008(spi, cs)

    def get_name(self):
        return self.NAME

    def _get_voltage(self) -> float:
        # create an analog input channel on pin 0
        chan = AnalogIn(self.mcp, mcp3008.P0)
        return chan.voltage

    def get_alcohol_level(self) -> float:
        return SMELLOSCOPE_OFFSET - self._get_voltage()

    def get_measurement(self) -> Measurement:
        time = datetime.datetime.now()
        alcohol_level = self.get_alcohol_level()
        measurement = Measurement(self.NAME, time, alcohol_level)
        return measurement
