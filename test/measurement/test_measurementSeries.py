import datetime
from unittest import TestCase

from autobrew.measurement.measurement import Measurement
from autobrew.measurement.measurementSeries import MeasurementSeries


class TestMeasurementSeries(TestCase):
    def test_get_name(self):
        series = MeasurementSeries(1, 'temp1')
        self.assertTrue(series.get_name())

    def test_to_json(self):
        series = MeasurementSeries(1, 'temp1')
        meas = Measurement('temp1', datetime.datetime.now(), 1.0)
        meas2 = Measurement('temp2', datetime.datetime.now(), 1.1)
        series.append(meas)
        series.append(meas2)
        self.assertTrue(series.to_json())