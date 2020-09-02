import time
import logging
from autobrew.dependencies import getTempSourceFactoryClass
from autobrew.measurement.measurementService import MeasurementService

SAMPLE_INTERVAL_SECONDS = 300
logger = logging.getLogger("autobrew")


def run_measurements(**kwargs):
    delay = kwargs.get("INTERVAL") or SAMPLE_INTERVAL_SECONDS
    measurement_service = MeasurementService()
    temp_factory = getTempSourceFactoryClass()()
    for iteration in range(0, 10):
        for source in temp_factory.get_all_temp_sources():
            measurement = source.get_temperature_measurement()
            measurement_service.save_measurement(measurement)
            logger.info("Temperature measurement taken: " + str(measurement))
        time.sleep(delay)
