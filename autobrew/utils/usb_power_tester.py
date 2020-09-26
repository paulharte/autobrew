from autobrew.heating.usb_api import switch_power
import sys


if __name__ == "__main__":
    on_off_arg = str(sys.argv[1])
    if on_off_arg == '0':
        switch_power(False)
        print("Power switched off")
    elif on_off_arg == '1':
        switch_power(True)
        print("power swtiched on")
    else:
        print("invalid args" + str(sys.argv))

