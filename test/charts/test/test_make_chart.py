import datetime
from unittest import TestCase

from autobrew.charts.make_chart import make_chart
from autobrew.measurement.measurement import Measurement
from autobrew.measurement.measurementSeries import MeasurementSeries
from autobrew.measurement.seriesType import SeriesType


class TestMakeChart(TestCase):
    def test_make_chart(self):
        series = MeasurementSeries("source", 1, SeriesType.TEMPERATURE)
        chart = make_chart(series)
        self.assertIsNotNone(chart)

        series.append(Measurement("source", datetime.datetime.now(), 20.1))
        chart2 = make_chart(series)
        self.assertIsNotNone(chart2)
