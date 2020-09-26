from autobrew.heating.usb_api import switch_power
import sys


if __name__ == "__main__":
    on_off_arg = sys.argv[0]
    if on_off_arg == 0:
        switch_power(False)
    elif on_off_arg == 1:
        switch_power(True)
