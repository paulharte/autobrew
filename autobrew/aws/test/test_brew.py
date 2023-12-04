import datetime
from unittest import TestCase
import json
from brew.brewRemote import BrewRemote
from brew.stages import FERMENTING


class TestBrew(TestCase):
    def test_brew(self):
        incoming = json.dumps(
            {
                "name": "brew1",
                "id": "1",
                "remote_id": "d2e85707-9fcf-4ff3-9d1b-bdb2419da674",
                "active": True,
                "stages": [
                    {
                        "start_time": "2021-05-15T19:30:54.100701",
                        "stage_name": "FERMENTING",
                        "estimated_end_time": "2021-05-22T19:30:54.100701",
                    }
                ],
            }
        )
        b = BrewRemote.from_json(incoming)
        self.assertEqual(b.name, "brew1")

        incoming2 = json.dumps(
            {
                "name": "brew2",
                "id": "2",
                "remote_id": "d2e85707-9fcf-4ff3-9d1b-bdb2419da675",
                "active": False,
                "stages": [
                    {
                        "start_time": "2021-05-15T19:30:54.100701",
                        "stage_name": "FERMENTING",
                        "estimated_end_time": "2021-05-22T19:30:54.100701",
                    }
                ],
            }
        )
        b2 = BrewRemote.from_json(incoming2)
        self.assertEqual(b2.name, "brew2")
        self.assertEqual(b2.active, False)
        self.assertEqual(b2.current_stage.stage_name, "FERMENTING")
        self.assertEqual(type(b2.current_stage.estimated_end_time), datetime.datetime)

    def test_dict(self):
        time_str = "2021-03-25T17:24:10.829080"
        incoming = json.dumps(
            {
                "name": "brew2",
                "id": "2",
                "remote_id": "d2e85707-9fcf-4ff3-9d1b-bdb2419da675",
                "active": False,
                "start_time": time_str,
                "current_stage": FERMENTING,
            }
        )
        b2 = BrewRemote.from_json(incoming)
        self.assertEqual(type(b2.start_time), datetime.datetime)
        b2dict = b2.to_dict()
        self.assertEqual(time_str, b2dict["start_time"])
        b2_final = BrewRemote.from_dict(b2dict)
        self.assertEqual(b2.start_time, b2_final.start_time)
        self.assertEqual(b2.remote_id, b2_final.remote_id)
        self.assertEqual(b2.id, b2_final.id)
        self.assertEqual(b2.active, b2_final.active)
