from autobrew.heating.usb_api import switch_power
import sys


if __name__ == "__main__":
    on_off_arg = str(sys.argv[1])
    if on_off_arg == "0":
        switch_power(False)
        print("power switched off")
    elif on_off_arg == "1":
        switch_power(True)
        print("power switched on")
    else:
        raise RuntimeError("invalid args, should be 1 or 0" + str(sys.argv))
