import busio
import digitalio
import adafruit_mcp3xxx.mcp3008 as mcp3008
from adafruit_mcp3xxx.analog_in import AnalogIn


class HardwareAlcoholSensor(object):

    mcp = None

    def setup_mcp(self):
        import board
        # create the spi bus
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

        # create the cs (chip select)
        cs = digitalio.DigitalInOut(board.D5)

        # create the mcp object
        self.mcp = mcp3008.MCP3008(spi, cs)

    def get_voltage(self) -> float:
        # This will throw exceptions in the event of a hardware issue
        if not self.mcp:
            self.setup_mcp()
        # create an analog input channel on pin 0
        chan = AnalogIn(self.mcp, mcp3008.P0)
        return chan.voltage
