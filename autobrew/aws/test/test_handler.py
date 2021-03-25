import datetime
from unittest import TestCase


from measurements.measurementServiceRemote import MeasurementServiceRemote
from brew.brewServiceRemote import BrewServiceRemote
from handler import *
from test_utils.stubDynamo import StubDynamo


class TestHandler(TestCase):
    def setUp(self) -> None:
        self.brew_service = BrewServiceRemote(StubDynamo())
        self.measurement_service = MeasurementServiceRemote(StubDynamo())

    def test_brew(self):
        remote_id = "d2e85707"
        event = make_event(
            {"name": "brew1", "id": "1", "remote_id": remote_id, "active": True}
        )
        resp = create_brew(event, None, self.brew_service)
        self.assertEqual(resp["statusCode"], 200)

        get_event = make_event(None, remote_id)
        resp = get_brew(get_event, remote_id, self.brew_service)
        self.assertEqual(resp["statusCode"], 200)
        resp = get_brews(get_event, remote_id, self.brew_service)
        self.assertEqual(resp["statusCode"], 200)
        self.assertEqual(len(json.loads(resp["body"])), 1)

        put_event = make_event(
            {"name": "brew1new", "id": "1", "remote_id": remote_id, "active": True},
            remote_id,
        )
        resp = update_brew(put_event, None, self.brew_service)
        self.assertEqual(resp["statusCode"], 200)
        resp = get_brew(get_event, remote_id, self.brew_service)
        self.assertEqual(resp["statusCode"], 200)
        self.assertEqual(BrewRemote.from_json(resp["body"]).name, "brew1new")

        delete_event = make_event(None, remote_id)
        resp = delete_brew(delete_event, None, self.brew_service)
        self.assertEqual(resp["statusCode"], 200)

        resp = get_brews(get_event, remote_id, self.brew_service)
        self.assertEqual(resp["statusCode"], 200)
        self.assertEqual(len(json.loads(resp["body"])), 0)

    def test_brew_error(self):
        event = make_event({})
        resp = create_brew(event, None, self.brew_service)
        self.assertEqual(resp["statusCode"], 400)
        resp = update_brew(event, None, self.brew_service)
        self.assertEqual(resp["statusCode"], 400)
        resp = delete_brew(event, None, self.brew_service)
        self.assertEqual(resp["statusCode"], 400)

    def test_series(self):
        remote_id = "d2e85707"
        temp_1 = "temperature1"
        event = make_series_event(
            {"source_name": temp_1, "brew_remote_id": "1", "measurements": [],},
            remote_id,
        )
        resp = create_measurements(event, None, self.measurement_service)
        self.assertEqual(resp["statusCode"], 200)

        get_event = make_series_event(None, remote_id, temp_1)
        resp = get_measurement_series(get_event, remote_id, self.measurement_service)
        self.assertEqual(resp["statusCode"], 200)
        resp = get_all_measurement_series(
            get_event, remote_id, self.measurement_service
        )
        self.assertEqual(resp["statusCode"], 200)
        self.assertEqual(len(json.loads(resp["body"])), 1)

        measurement = {
            "source_name": "temperature1",
            "measurement_amt": 20.1,
            "time": str(datetime.datetime(2021, 1, 31, 13, 10)),
        }

        put_event = make_series_event(
            {
                "source_name": "temperature1",
                "brew_id": "1",
                "brew_remote_id": remote_id,
                "measurements": [measurement],
            },
            remote_id,
            temp_1,
        )
        resp = update_measurements(put_event, None, self.measurement_service)

        self.assertEqual(resp["statusCode"], 200)
        resp = get_measurement_series(get_event, remote_id, self.measurement_service)
        self.assertEqual(resp["statusCode"], 200)
        output = MeasurementSeriesRemote.from_json(resp["body"])
        self.assertEqual(output.source_name, "temperature1")
        self.assertEqual(output.measurements[0].measurement_amt, 20.1)

        delete_event = make_series_event(None, remote_id, temp_1)
        resp = delete_measurements(delete_event, None, self.measurement_service)
        self.assertEqual(resp["statusCode"], 200)

        resp = get_all_measurement_series(
            get_event, remote_id, self.measurement_service
        )
        self.assertEqual(resp["statusCode"], 200)
        self.assertEqual(len(json.loads(resp["body"])), 0)

    def test_series_error(self):
        event = make_event({})
        resp = update_measurements(event, None, self.measurement_service)
        self.assertEqual(resp["statusCode"], 400)
        resp = delete_measurements(event, None, self.measurement_service)
        self.assertEqual(resp["statusCode"], 400)

    def test_series_get_measurements_for_brew(self):
        remote_id = "d2e85707"
        temp_1 = "temperature1"
        smelloscope = "smelloscope1"
        other_brew = "someOtherBrew12345"
        self._create_series(temp_1, remote_id)
        self._create_series(smelloscope, remote_id)
        self._create_series(smelloscope, other_brew)

        event = make_series_event(None, remote_id, None)
        resp = get_measurement_series_for_brew(event, None, self.measurement_service)
        self.assertEqual(len(json.loads(resp["body"])), 2)

        event = make_series_event(None, other_brew, None)
        resp = get_measurement_series_for_brew(event, None, self.measurement_service)
        self.assertEqual(len(json.loads(resp["body"])), 1)

    def _create_series(self, source_name: str, remote_id: str):
        event = make_series_event(
            {
                "source_name": source_name,
                "brew_id": "1",
                "brew_remote_id": remote_id,
                "measurements": [],
            },
            remote_id,
        )
        resp = create_measurements(event, None, self.measurement_service)
        self.assertEqual(resp["statusCode"], 200)


def make_event(payload: dict, brew_remote_id: str = None):
    out = {"pathParameters": {}, "body": json.dumps(payload)}
    if brew_remote_id:
        out["pathParameters"] = {"brew_remote_id": brew_remote_id}
    return out


def make_series_event(
    payload: dict, brew_remote_id: str = None, source_name: str = None
):
    out = {"pathParameters": {}, "body": json.dumps(payload)}
    if brew_remote_id:
        out["pathParameters"]["brew_remote_id"] = brew_remote_id
    if source_name:
        out["pathParameters"]["source_name"] = source_name
    return out
