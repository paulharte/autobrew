import time
import logging

from injector import inject, singleton

from autobrew.brew_settings import SAMPLE_INTERVAL_SECONDS
from autobrew.dependencies import getTempSourceFactoryClass, getSmellClass
from autobrew.heating.heat_control import HeatControl
from autobrew.measurement.measurementService import MeasurementService
from autobrew.smelloscope.smelloscope import Smelloscope
from autobrew.temperature.tempSourceFactory import TempSourceFactory

logger = logging.getLogger("autobrew")


class MeasurementTaker(object):
    @singleton
    @inject
    def __init__(
        self,
        temp_factory: TempSourceFactory,
        smell_source: Smelloscope,
        heat_control: HeatControl,
        measurement_service: MeasurementService,
    ):
        self.temp_factory = temp_factory
        self.smell_source = smell_source
        self.heat_control = heat_control
        self.measurement_service = measurement_service

    def run_measurements(self):
        delay = SAMPLE_INTERVAL_SECONDS
        while True:
            for source in self.temp_factory.get_all_temp_sources():
                try:
                    measurement = source.get_temperature_measurement()
                    self.measurement_service.save_measurement(measurement)
                    logger.info("Temperature measurement taken: " + str(measurement))
                    if source.is_primary:
                        self.heat_control.adjust(measurement.measurement_amt)

                except OSError as e:
                    logger.error("Could not take temperature measurement")
                    logger.exception(e)
                    self.temp_factory.remove_temp_source(source)

            smell_measurement = self.smell_source.get_measurement()
            self.measurement_service.save_measurement(smell_measurement)
            logger.info("Alcohol measurement taken: " + str(smell_measurement))
            time.sleep(delay)
