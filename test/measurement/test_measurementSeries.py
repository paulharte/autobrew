import datetime
import json
from unittest import TestCase

from autobrew.measurement.measurement import Measurement
from autobrew.measurement.measurementSeries import MeasurementSeries
from autobrew.measurement.seriesType import SeriesType


class TestMeasurementSeries(TestCase):
    def test_get_name(self):
        series = MeasurementSeries("temp1", 1, SeriesType.ALCOHOL)
        self.assertTrue(series.get_name())

    def test_to_json(self):
        series = MeasurementSeries("temp1", 1, SeriesType.TEMPERATURE)
        meas = Measurement("temp1", datetime.datetime.now(), 1.0)
        meas2 = Measurement("temp2", datetime.datetime.now(), 1.1)
        series.append(meas)
        series.append(meas2)
        j = series.to_json()
        self.assertTrue(j)
        out = json.loads(j)
        self.assertEqual(out["type"], "TEMPERATURE")
        self.assertEqual(out["source_name"], "temp1")
