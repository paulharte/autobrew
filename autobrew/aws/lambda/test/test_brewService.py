import json
from unittest import TestCase
from .stubDynamo import StubDynamo
from ..brew.brewServiceRemote import BrewServiceRemote
from ..brew.brewRemote import BrewRemote


class TestBrewService(TestCase):
    def test_put(self):
        mock_dynamo = StubDynamo()
        service = BrewServiceRemote(mock_dynamo)

        brew = BrewRemote.from_json(
            json.dumps(
                {"name": "brew2", "id": "2", "active": False, "remote_id": "xyz1"}
            )
        )
        service.create(brew)
        brews = service.getAll()

        self.assertEqual(1, len(brews))
        self.assertEqual(brews[0].name, "brew2")

        brew.name = "newbrew"
        service.put(brew)
        brews = service.getAll()

        self.assertEqual(1, len(brews))
        self.assertEqual(brews[0].name, "newbrew")

    def test_delete(self):
        service = BrewServiceRemote(StubDynamo())

        brew = BrewRemote.from_json(
            json.dumps(
                {"name": "brew2", "id": "2", "active": False, "remote_id": "xyz1"}
            )
        )
        service.create(brew)
        brews = service.getAll()
        self.assertEqual(1, len(brews))
        self.assertEqual(brews[0].name, "brew2")

        service.delete("xyz1")

        brews = service.getAll()
        self.assertEqual(0, len(brews))
