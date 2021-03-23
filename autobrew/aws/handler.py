import json
from autobrew.aws.brew.brewRemote import BrewRemote
from autobrew.aws.brew.brewServiceRemote import make_brew_service
from autobrew.aws.measurements.measurementServiceRemote import make_measurement_service
from autobrew.aws.measurements.measurementSeriesRemote import MeasurementSeriesRemote
import logging
logging.basicConfig(level=logging.INFO)



def create_brew(event: dict, context, service=None):
    if not service:
        service = make_brew_service()
    brew = BrewRemote.from_json(event["body"])
    service.create(brew)
    return {"statusCode": 200}


def get_brews(event: dict, context, service=None):
    if not service:
        service = make_brew_service()
    brews = service.getAll()
    return {"statusCode": 200, "body": json.dumps(brews, default=lambda o: o.to_json())}


def get_brew(event: dict, context, service=None):
    if not service:
        service = make_brew_service()
    id_to_get = event["pathParameters"]["brew_remote_id"]
    brew = service.get(id_to_get)

    if not brew:
        return {"statusCode": 404, "body": json.dumps({"error": "Brew does not exist"})}

    return {"statusCode": 200, "body": brew.to_json()}


def update_brew(event: dict, context, service=None):
    if not service:
        service = make_brew_service()
    brew = BrewRemote.from_json(event["body"])
    service.put(brew)
    return {"statusCode": 200}


def delete_brew(event: dict, context, service=None):
    if not service:
        service = make_brew_service()
    id_to_delete = event["pathParameters"]["brew_remote_id"]
    service.delete(id_to_delete)
    return {"statusCode": 200}


## Measurements


def create_measurements(event: dict, context, service=None):
    if not service:
        service = make_measurement_service()
    series = MeasurementSeriesRemote.from_json(event["body"])
    series.brew_remote_id = event["pathParameters"]["brew_remote_id"]
    response = service.create(series)
    return {"statusCode": 200}


def get_all_measurement_series(event: dict, context, service=None):
    if not service:
        service = make_measurement_service()
    series = service.getAll()
    return {
        "statusCode": 200,
        "body": json.dumps(series, default=lambda o: o.to_json()),
    }


def get_measurement_series(event: dict, context, service=None):
    if not service:
        service = make_measurement_service()
    brew_remote_id = event["pathParameters"]["brew_remote_id"]
    source_name = event["pathParameters"]["source_name"]
    series = service.get(brew_remote_id, source_name)

    if not series:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Measurement series does not exist"}),
        }

    return {"statusCode": 200, "body": series.to_json()}


def get_measurement_series_for_brew(event: dict, context, service=None):
    if not service:
        service = make_measurement_service()
    brew_remote_id = event["pathParameters"]["brew_remote_id"]
    series = service.get_all_for_brew(brew_remote_id)

    if not series:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Measurement series does not exist"}),
        }

    return {
        "statusCode": 200,
        "body": json.dumps(series, default=lambda o: o.to_json()),
    }


def update_measurements(event: dict, context, service=None):
    if not service:
        service = make_measurement_service()
    series = MeasurementSeriesRemote.from_json(event["body"])
    series.brew_remote_id = event["pathParameters"]["brew_remote_id"]
    service.put(series)
    return {"statusCode": 200}


def delete_measurements(event: dict, context, service=None):
    if not service:
        service = make_measurement_service()
    brew_remote_id = event["pathParameters"]["brew_remote_id"]
    source_name = event["pathParameters"]["source_name"]
    service.delete(brew_remote_id, source_name)
    return {"statusCode": 200}
