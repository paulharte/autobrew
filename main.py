import sys
import threading
import logging

from autobrew.measurement_taker import run_measurements
from autobrew.webserver import run_webserver


def set_logging(level=logging.DEBUG):
    logger = logging.getLogger("autobrew")
    logger.setLevel(level)
    logger.debug("Log level set to " + str(level))
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setLevel(level)
    logger.addHandler(handler)


if __name__ == "__main__":
    set_logging()
    x = threading.Thread(target=run_webserver, args=(False,), daemon=True)
    x.start()
    run_measurements()
