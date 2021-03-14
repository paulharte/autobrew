from typing import List

import boto3
from boto3.dynamodb.conditions import Key

DYNAMO_DB = "dynamodb"
REGION = "eu-west-1"


class Dynamo(object):
    def __init__(self):
        self.dynamo_db = boto3.resource(DYNAMO_DB, region_name=REGION)

    def get_all(self, table_name: str) -> List:
        table = self.dynamo_db.Table(table_name)
        return table.scan()

    def put(self, table_name: str, item: dict):
        table = self.dynamo_db.Table(table_name)

        return table.put_item(Item=item)

    def get(self, table_name: str, id_to_get, id_name):
        key = _form_key(id_to_get, id_name)
        return self.dynamo_db.get_item(TableName=table_name, Key=key).get("Item")

    def get_many(self, table_name: str, id_to_get: str, id_name: str) -> List:
        table = self.dynamo_db.Table(table_name)
        filtering_exp = Key(id_name).eq(id_to_get)
        out = table.query(filtering_exp)
        return out.get('Items')

    def delete(self, table_name: str, id_to_delete: str, id_name: str):
        table = self.dynamo_db.Table(table_name)
        key = _form_key(id_to_delete, id_name)
        resp = table.delete_item(Key=key)
        return resp


def _form_key(id_to_get, id_name):
    if type(id_to_get) == list:
        key = {}
        for id_single, name in zip(id_to_get, id_name):
            key[name] = id_single
        return key
    else:
        return {id_name: id_to_get}
