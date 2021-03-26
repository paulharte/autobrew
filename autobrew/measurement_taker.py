import time
import logging

from injector import inject, singleton

from autobrew.alerting.alerter import Alerter
from autobrew.brew.brew import Brew
from autobrew.brew.brewService import BrewService
from autobrew.brew_settings import SAMPLE_INTERVAL_SECONDS, APP_LOGGING_NAME
from autobrew.heating.heat_control import HeatControl
from autobrew.measurement.measurementService import MeasurementService
from autobrew.smelloscope.smelloscope import SmelloscopeNotAvailable
from autobrew.smelloscope.smelloscopeFactory import SmelloscopeFactory
from autobrew.sync.syncService import SyncService
from autobrew.temperature.probeTempApi import InvalidTemperatureFileError
from autobrew.temperature.tempSourceFactory import TempSourceFactory

logger = logging.getLogger(APP_LOGGING_NAME)


class MeasurementTaker(object):
    @singleton
    @inject
    def __init__(
        self,
        brew_service: BrewService,
        temp_factory: TempSourceFactory,
        smell_factory: SmelloscopeFactory,
        heat_control: HeatControl,
        measurement_service: MeasurementService,
        alerter: Alerter,
        sync: SyncService,
    ):
        self.brew_service = brew_service
        self.temp_factory = temp_factory
        self.smell_factory = smell_factory
        self.heat_control = heat_control
        self.measurement_service = measurement_service
        self.alerter = alerter
        self.sync = sync

    def run_measurements(self):
        delay = SAMPLE_INTERVAL_SECONDS
        active_brew = self.brew_service.get_active()
        if active_brew:
            self.sync.sync_brew(active_brew)
        while True:
            active_brew = self.brew_service.get_active()
            if active_brew:
                self.take_temperature_measurements(active_brew)
                self.take_smell_measurements(active_brew)
            time.sleep(delay)

    def take_temperature_measurements(self, brew: Brew):
        for source in self.temp_factory.get_all_temp_sources():
            try:
                measurement = source.get_temperature_measurement()
                series = self.measurement_service.save_measurement(measurement, brew)
                logger.info("Temperature measurement taken: " + str(measurement))
                self.sync.sync_measurements(brew, series)
                if source.is_primary:
                    self.heat_control.adjust(measurement.measurement_amt)

            except (OSError, InvalidTemperatureFileError) as e:
                msg = (
                    "Could not take temperature measurement due to exception %s"
                    % type(e)
                )
                logger.error(msg)
                logger.exception(e)
                self.temp_factory.remove_temp_source(source)
                self.alerter.alert_owner(msg)

    def take_smell_measurements(self, brew: Brew):
        for smell_source in self.smell_factory.get_all_sources():
            try:
                smell_measurement = smell_source.get_measurement()
                series = self.measurement_service.save_measurement(
                    smell_measurement, brew
                )
                logger.info("Alcohol measurement taken: " + str(smell_measurement))
                self.sync.sync_measurements(brew, series)
            except SmelloscopeNotAvailable as e:
                msg = "No alcohol measurement taken as smelloscope offline" + str(e)
                logger.error(msg)
                self.alerter.alert_owner(msg)
