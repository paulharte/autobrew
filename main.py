import sys
import threading
import logging

from injector import Injector

from autobrew.brew_settings import APP_LOGGING_NAME
from autobrew.dependencies import configure
from autobrew.measurement_taker import MeasurementTaker
from autobrew.webserver import run_webserver


def set_logging(level=logging.DEBUG):
    logger = logging.getLogger(APP_LOGGING_NAME)
    logger.setLevel(level)
    logger.debug("Log level set to " + str(level))
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setLevel(level)
    logger.addHandler(handler)


if __name__ == "__main__":
    set_logging()
    autobrew_injector = Injector([configure])
    x = threading.Thread(
        target=run_webserver, args=(autobrew_injector, False), daemon=True
    )
    x.start()
    autobrew_injector.get(MeasurementTaker).run_measurements()
