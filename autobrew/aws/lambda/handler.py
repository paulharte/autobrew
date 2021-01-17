
import json
from .brew import Brew
from .brewService import BrewService

def create_brew(event: dict, context):
    brew = Brew.from_json(event['body'])
    response = BrewService().create(brew)
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }


def get_brews(event: dict, context):
    brews = BrewService().getAll()
    return {
        'statusCode': 200,
        'body': json.dumps(brews)
    }

def get_brew(event: dict , context):
    id_to_get = event['pathParameters']['id']
    brew = BrewService().get(id_to_get)

    if not brew:
        return {'statusCode': 404, 'body': json.dumps({'error': 'Brew does not exist'})}

    return {
        'statusCode': 200,
        'body': brew.to_json()
    }

def update_brew(event, context):
    brew = Brew.from_json(event['body'])
    response = BrewService().put(brew)
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

def delete_brew(event, context):
    id_to_delete = event['pathParameters']['id']
    response = BrewService().delete(id_to_delete)
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

