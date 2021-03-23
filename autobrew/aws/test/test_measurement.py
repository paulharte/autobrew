from unittest import TestCase
import json
from autobrew.aws.measurements.measurementSeriesRemote import MeasurementSeriesRemote


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
