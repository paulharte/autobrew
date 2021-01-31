from unittest import TestCase

from injector import Injector

from autobrew.configuration import configure_test
from autobrew.measurement.measurementService import MeasurementService
from autobrew.measurement_taker import MeasurementTaker
from autobrew.smelloscope.smelloscope import Smelloscope
from autobrew.temperature.tempSource import PROBE_PREFIX
from test.temperature.stubProbeApi import STUB_BREW_NAME, STUB_ROOM_NAME


class TestMeasurementTaker(TestCase):
    def test_take_alcohol(self):
        injector = Injector([configure_test])
        taker = injector.get(MeasurementTaker)

        taker.take_smell_measurements()
        taker.take_smell_measurements()
        measure_service = injector.get(MeasurementService)
        series = measure_service.get_series(Smelloscope.NAME)

        self.assertEqual(len(series.get_measurements()), 2)

    def test_take_temp(self):
        injector = Injector([configure_test])
        taker = injector.get(MeasurementTaker)

        taker.take_temperature_measurements()
        measure_service = injector.get(MeasurementService)

        brew_series = measure_service.get_series(PROBE_PREFIX + STUB_BREW_NAME)
        self.assertEqual(len(brew_series.get_measurements()), 1)

        room_series = measure_service.get_series(PROBE_PREFIX + STUB_ROOM_NAME)
        self.assertEqual(len(room_series.get_measurements()), 1)
