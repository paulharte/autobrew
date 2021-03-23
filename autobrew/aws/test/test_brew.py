from unittest import TestCase
import json
from autobrew.aws.brew.brewRemote import BrewRemote


class TestBrew(TestCase):
    def test_brew(self):
        incoming = json.dumps(
            {
                "name": "brew1",
                "id": "1",
                "remote_id": "d2e85707-9fcf-4ff3-9d1b-bdb2419da674",
                "active": True,
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
            }
        )
        b2 = BrewRemote.from_json(incoming2)
        self.assertEqual(b2.name, "brew2")
        self.assertEqual(b2.active, False)
