import datetime
from unittest import TestCase
import json

from measurements.measurementRemote import MeasurementRemote
from measurements.measurementSeriesRemote import MeasurementSeriesRemote


class TestMeasurementSeriesRemote(TestCase):
    def test_series(self):
        incoming = json.dumps(
            {
                "source_name": "temperature1",
                "brew_id": "1",
                "brew_remote_id": "d2e85707-9fcf-4ff3-9d1b-bdb2419da674",
                "measurements": [],
            }
        )
        b = MeasurementSeriesRemote.from_json(incoming)
        self.assertEqual(b.source_name, "temperature1")

        incoming2 = json.dumps(
            {
                "source_name": "smelloscope",
                "brew_id": "1",
                "brew_remote_id": "d2e85707-9fcf-4ff3-9d1b-bdb2419da674",
                "measurements": [],
            }
        )
        b2 = MeasurementSeriesRemote.from_json(incoming2)
        self.assertEqual(b2.source_name, "smelloscope")

    def test_todict(self):
        incoming = json.dumps(
            {
                "source_name": "temperature1",
                "brew_id": "1",
                "brew_remote_id": "d2e85707-9fcf-4ff3-9d1b-bdb2419da674",
                "measurements": [],
            }
        )
        series = MeasurementSeriesRemote.from_json(incoming)
        meas = MeasurementRemote()
        meas.time = datetime.datetime.now()
        meas.source_name = series.source_name
        meas.measurement_amt = 20.1
        series.measurements = [meas]
        d = series.to_dict()
        self.assertEqual(str, type(d["measurements"][0]["time"]))
        series_out = MeasurementSeriesRemote.from_dict(d)
        self.assertEqual(meas.time, series_out.measurements[0].time)
        self.assertEqual(
            meas.measurement_amt, series_out.measurements[0].measurement_amt
        )
        self.assertEqual(meas.source_name, series_out.measurements[0].source_name)
        self.assertEqual(series.brew_remote_id, series_out.brew_remote_id)
