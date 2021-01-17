from typing import List

import boto3
from .brew import Brew

BREWS_DYNAMO_TABLE = 'autobrew_brew'
DYNAMO_DB = 'dynamodb'
dynamodb = boto3.resource(DYNAMO_DB)



class BrewService(object):
    #TODO: would be nice to further abstract dynamo away from this

    def getAll(self) -> List:
        table = dynamodb.Table(BREWS_DYNAMO_TABLE)
        return table.scan()

    def put(self, brew: Brew):
        table = dynamodb.Table(BREWS_DYNAMO_TABLE)

        return table.put_item(Item=brew.to_dict())

    def get(self, id_to_get) -> Brew:
        resp =  dynamodb.get_item(
            TableName=BREWS_DYNAMO_TABLE,
            Key={
                'id': {'S': id_to_get}
            }
        )
        return Brew.from_dict(resp.get('Item'))

    def create(self, brew:Brew):
        return self.put(brew)

    def delete(self, id: str):
        resp = dynamodb.get_item(
            TableName=BREWS_DYNAMO_TABLE,
            Key={
                'id': {'S': id}
            })
        return resp