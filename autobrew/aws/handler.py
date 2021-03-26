import json
from json import JSONDecodeError

from brew.brewRemote import BrewRemote
from brew.brewServiceRemote import make_brew_service
from measurements.measurementServiceRemote import make_measurement_service
from measurements.measurementSeriesRemote import MeasurementSeriesRemote
import logging

from storage.serializable import default_convert_to_json

logging.basicConfig(level=logging.INFO)


def create_brew(event: dict, context, service=None):
    if not service:
        service = make_brew_service()
    try:
        brew = BrewRemote.from_json(event["body"])
    except (ValueError, JSONDecodeError, KeyError) as e:
        return handle_error(e)
    service.create(brew)
    return {"statusCode": 200}


def get_brews(event: dict, context, service=None):
    if not service:
        service = make_brew_service()
    brews = service.getAll()
    return {"statusCode": 200, "body": json.dumps(brews, default=default_convert_to_json)}


def get_brew(event: dict, context, service=None):
    if not service:
        service = make_brew_service()
    try:
        id_to_get = event["pathParameters"]["brew_remote_id"]
    except KeyError as e:
        return handle_error(e)
    brew = service.get(id_to_get)

    if not brew:
        return {"statusCode": 404, "body": json.dumps({"error": "Brew does not exist"})}

    return {"statusCode": 200, "body": brew.to_json()}


def update_brew(event: dict, context, service=None):
    if not service:
        service = make_brew_service()
    try:
        brew = BrewRemote.from_json(event["body"])
    except (ValueError, JSONDecodeError, KeyError) as e:
        return handle_error(e)
    service.put(brew)
    return {"statusCode": 200}


def delete_brew(event: dict, context, service=None):
    if not service:
        service = make_brew_service()
    try:
        id_to_delete = event["pathParameters"]["brew_remote_id"]
    except KeyError as e:
        return handle_error(e)
    service.delete(id_to_delete)
    return {"statusCode": 200}


## Measurements


def create_measurements(event: dict, context, service=None):
    if not service:
        service = make_measurement_service()
    try:
        series = MeasurementSeriesRemote.from_json(event["body"])
        series.brew_remote_id = event["pathParameters"]["brew_remote_id"]
    except (ValueError, JSONDecodeError, KeyError) as e:
        return handle_error(e)
    service.create(series)
    return {"statusCode": 200}


def get_all_measurement_series(event: dict, context, service=None):
    if not service:
        service = make_measurement_service()
    series = service.getAll()
    return {
        "statusCode": 200,
        "body": json.dumps(series, default=default_convert_to_json)
    }


def get_measurement_series(event: dict, context, service=None):
    if not service:
        service = make_measurement_service()
    try:
        brew_remote_id = event["pathParameters"]["brew_remote_id"]
        source_name = event["pathParameters"]["source_name"]
    except KeyError as e:
        return handle_error(e)
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
    try:
        brew_remote_id = event["pathParameters"]["brew_remote_id"]
    except KeyError as e:
        return handle_error(e)
    series = service.get_all_for_brew(brew_remote_id)

    if not series:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Measurement series does not exist"}),
        }

    return {
        "statusCode": 200,
        "body": json.dumps(series, default=default_convert_to_json)
    }


def update_measurements(event: dict, context, service=None):
    if not service:
        service = make_measurement_service()
    try:
        series = MeasurementSeriesRemote.from_json(event["body"])
        series.brew_remote_id = event["pathParameters"]["brew_remote_id"]
    except (ValueError, JSONDecodeError, KeyError) as e:
        return handle_error(e)
    service.put(series)
    return {"statusCode": 200}


def delete_measurements(event: dict, context, service=None):
    if not service:
        service = make_measurement_service()
    try:
        brew_remote_id = event["pathParameters"]["brew_remote_id"]
        source_name = event["pathParameters"]["source_name"]
    except KeyError as e:
        return handle_error(e)
    service.delete(brew_remote_id, source_name)
    return {"statusCode": 200}


def handle_error(e: Exception):
    return {"statusCode": 400, "body": "Bad input %s" % e}
