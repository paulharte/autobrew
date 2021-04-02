from unittest import TestCase

from injector import Injector

from autobrew.brew.brewService import BrewService
from autobrew.configuration import configure_test
from autobrew.measurement.measurementService import MeasurementService
from autobrew.measurement_taker import MeasurementTaker
from autobrew.smelloscope.smelloscope import Smelloscope
from autobrew.temperature.tempSource import PROBE_PREFIX
from test.temperature.stubProbeApi import STUB_BREW_TEMP_NAME, STUB_ROOM_TEMP_NAME


class TestMeasurementTaker(TestCase):
    def setUp(self) -> None:
        self.injector = Injector([configure_test])
        self.brew_service = self.injector.get(BrewService)
        self.brew = self.brew_service.new("MyBrew")

    def test_take_alcohol(self):

        taker = self.injector.get(MeasurementTaker)

        taker.take_smell_measurements(self.brew)
        taker.take_smell_measurements(self.brew)
        measure_service = self.injector.get(MeasurementService)
        series = measure_service.get_series_by_source(Smelloscope.NAME, self.brew.id)

        self.assertEqual(len(series.get_measurements()), 2)

    def test_take_temp(self):
        taker = self.injector.get(MeasurementTaker)

        taker.take_temperature_measurements(self.brew)
        measure_service = self.injector.get(MeasurementService)

        brew_series = measure_service.get_series_by_source(
            PROBE_PREFIX + STUB_BREW_TEMP_NAME, self.brew.id
        )
        self.assertEqual(len(brew_series.get_measurements()), 1)

        room_series = measure_service.get_series_by_source(
            PROBE_PREFIX + STUB_ROOM_TEMP_NAME, self.brew.id
        )
        self.assertEqual(len(room_series.get_measurements()), 1)
