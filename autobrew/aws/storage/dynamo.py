import logging
from typing import List

import boto3
from boto3.dynamodb.conditions import Key

DYNAMO_DB = "dynamodb"
REGION = "eu-west-1"

logger = logging.getLogger()


class Dynamo(object):
    def __init__(self):
        self.dynamo_db = boto3.resource(DYNAMO_DB, region_name=REGION)

    def get_all(self, table_name: str) -> List:
        table = self.dynamo_db.Table(table_name)
        return table.scan().get("Items")

    def put(self, table_name: str, item: dict):
        item = delete_nulls_from_dict(item)
        table = self.dynamo_db.Table(table_name)
        try:
            table.put_item(Item=item)
            logger.info("Item written  to Dynamo table: %s. Item: %s", table_name, item)
        except Exception as e:
            logger.error("Could not write to Dynamo!. Payload:%s" % item)
            raise e

    def get(self, table_name: str, id_to_get, id_name) -> dict:
        key = _form_key(id_to_get, id_name)
        return self.dynamo_db.get_item(TableName=table_name, Key=key).get("Item")

    def get_many(self, table_name: str, id_to_get: str, id_name: str) -> List[dict]:
        table = self.dynamo_db.Table(table_name)
        filtering_exp = Key(id_name).eq(id_to_get)
        out = table.query(KeyConditionExpression=filtering_exp)
        return out.get("Items")

    def delete(self, table_name: str, id_to_delete: str, id_name: str):
        table = self.dynamo_db.Table(table_name)
        key = _form_key(id_to_delete, id_name)
        resp = table.delete_item(Key=key)
        logger.info(
            "Item deleted from to Dynamo table: %s. Item: %s", table_name, id_to_delete
        )


def _form_key(id_to_get, id_name):
    if type(id_to_get) == list:
        key = {}
        for id_single, name in zip(id_to_get, id_name):
            key[name] = id_single
        return key
    else:
        return {id_name: id_to_get}


def delete_nulls_from_dict(d: dict) -> dict:
    to_delete = []
    for key, value in d.items():
        if value is None:
            to_delete.append(key)
    for null_item in to_delete:
        del d[null_item]
    return d
