import os

from autobrew.utils.detect_pi_model import detect_pi_model
import logging

LOGGER = logging.getLogger()


def switch_power(on: bool):

    on_off = "1" if on else "0"
    commands = {
        4: "uhubctl -l 1-1 -p 1 -a ",
        3: "uhubctl -l 1-1 -p 2 -a ",
        2: "uhubctl -l 1-1 -p 2 -a ",
    }
    command = commands.get(detect_pi_model())

    out = os.system(command + on_off)

    if out == 0:
        LOGGER.info("USB power switched to %s" % ("on" if on else "off"))
        return
    else:
        raise PowerSwitchException("got error when switching power. Code: %d" % out)


class PowerSwitchException(Exception):
    pass
