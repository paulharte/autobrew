from unittest import TestCase
import json
from .brew import Brew


class TestBrew(TestCase):
    def test_brew(self):
        incoming = json.dumps({"name": "brew1", "id": "1", "active": True})
        b = Brew.from_json(incoming)
        self.assertEqual(b.name, "brew1")

        incoming2 = json.dumps({"name": "brew2", "id": "2"})
        b2 = Brew.from_json(incoming2)
        self.assertEqual(b2.name, "brew2")
        self.assertEqual(b2.active, False)
