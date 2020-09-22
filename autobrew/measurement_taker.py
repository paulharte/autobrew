import time
import logging
from autobrew.dependencies import getTempSourceFactoryClass, getSmellClass
from autobrew.measurement.measurementService import MeasurementService

SAMPLE_INTERVAL_SECONDS = 120
logger = logging.getLogger("autobrew")


def run_measurements(**kwargs):
    delay = kwargs.get("INTERVAL") or SAMPLE_INTERVAL_SECONDS
    measurement_service = MeasurementService()
    temp_factory = getTempSourceFactoryClass()()
    smell_source = getSmellClass()()
    while True:
        for source in temp_factory.get_all_temp_sources():
            measurement = source.get_temperature_measurement()
            measurement_service.save_measurement(measurement)
            logger.info("Temperature measurement taken: " + str(measurement))

        smell_measurement = smell_source.get_measurement()
        measurement_service.save_measurement(smell_measurement)
        logger.info("Alcohol measurement taken: " + str(smell_measurement))
        time.sleep(delay)

