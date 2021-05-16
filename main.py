import sys
import threading
import logging

from injector import Injector

from autobrew.brew_settings import APP_LOGGING_NAME
from autobrew.configuration import configure_prod, configure_uat
from autobrew.measurement_taker import MeasurementTaker
from autobrew.webserver import run_webserver


def set_logging(level=logging.DEBUG):
    logger = logging.getLogger(APP_LOGGING_NAME)
    logger.setLevel(level)
    logger.debug("Log level set to " + str(level))
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setLevel(level)
    logger.addHandler(handler)


def main():
    set_logging()
    if (len(sys.argv) > 1) and (sys.argv[1] == "prod"):
        autobrew_injector = Injector([configure_prod])
    else:
        autobrew_injector = Injector([configure_uat])
    x = threading.Thread(
        target=run_webserver, args=(autobrew_injector, False), daemon=True
    )
    x.start()
    autobrew_injector.get(MeasurementTaker).run_measurements()


if __name__ == "__main__":
    main()
