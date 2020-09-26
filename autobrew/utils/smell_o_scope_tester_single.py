import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as mcp3008
from adafruit_mcp3xxx.analog_in import AnalogIn

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = mcp3008.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan = AnalogIn(mcp, mcp3008.P0)

print("Raw ADC Value: ", chan.value)
print("ADC Voltage: " + str(chan.voltage) + "V")
