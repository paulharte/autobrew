import datetime
import json
from unittest import TestCase

from autobrew.brew.brew import Brew, sort_brews
from autobrew.aws.storage.serializable import Serializable


class TestBrew(TestCase):
    def test_newbrew(self):
        before = datetime.datetime(2021, 2, 1, 18, 00)
        later = datetime.datetime(2021, 2, 21, 18, 00)
        brew1 = Brew("one", before)
        brew2 = Brew("two", before)
        brew3 = Brew("three", later)
        brew2.active = True
        brew1.active = False

        arr = sort_brews([brew1, brew2, brew3])
        self.assertEqual(
            "two", arr[0].name,
        )
        self.assertEqual(
            "three", arr[1].name,
        )

    def test_to_json(self):
        before = datetime.datetime(2021, 2, 1, 18, 00)
        brew1 = Brew("one", before)
        brew2 = Brew("two", before)

        self.assertTrue(brew1.to_json())
        self.assertTrue(brew2.to_json())

        out = json.loads(brew1.to_json())
        self.assertEqual(out["name"], "one")
        self.assertEqual(out["current_stage"], "FERMENTING")

    def test_from_json(self):
        before = datetime.datetime(2021, 2, 1, 18, 00)
        brew1 = Brew("one", before)
        brew1.remote_id = "12345"  # need to have this id before sending

        self.assertTrue(brew1.to_json())
        decoded = Serializable.from_json(brew1.to_json())
        self.assertTrue(decoded)
        self.assertEqual(decoded.name, "one")
        self.assertEqual(decoded.start_time, before)
