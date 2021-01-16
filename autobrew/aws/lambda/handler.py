
import json
import boto3

BREWS_DYNAMO_TABLE = 'autobrew_brew'
DYNAMO_DB = 'dynamodb'


def create_brew(event, context):
    dynamodb = boto3.resource(DYNAMO_DB)
    table = dynamodb.Table(BREWS_DYNAMO_TABLE)

    brew = {'id': event['name'],
            'active': event.get('active', False),
            'name': event['name']}
    response = table.put_item(Item=brew)

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }


def get_brews(event, context):
    dynamodb = boto3.resource(DYNAMO_DB)
    table = dynamodb.Table(BREWS_DYNAMO_TABLE)
    brews = table.scan()
    return {
        'statusCode': 200,
        'body': json.dumps(brews)
    }

