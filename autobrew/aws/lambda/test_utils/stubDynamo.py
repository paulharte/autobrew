from typing import List

from measurements.measurementServiceRemote import MEASUREMENT_SERIES_DYNAMO_TABLE
from brew.brewServiceRemote import BREWS_DYNAMO_TABLE, BREW_TABLE_ID


class StubDynamo(object):
    def __init__(self):
        self.dynamo_db = {BREWS_DYNAMO_TABLE: {}, MEASUREMENT_SERIES_DYNAMO_TABLE: {}}

    def get_all(self, table_name: str) -> List:
        table: dict = self.dynamo_db.get(table_name)
        return list(table.values())

    def put(self, table_name: str, item: dict):
        table: dict = self.dynamo_db.get(table_name)
        key = _get_key(table_name, item)
        table[key] = item

    def get(self, table_name: str, id_to_get, id_name):
        key = _form_key(id_to_get, id_name)
        table: dict = self.dynamo_db.get(table_name)
        return table.get(key)

    def get_many(self, table_name: str, id_to_get: str, id_name: str) -> List:
        key_to_find = _form_key(id_to_get, id_name)
        table: dict = self.dynamo_db.get(table_name)
        out = []
        for key in table.keys():
            if key_to_find in key:
                out.append(table[key])
        return out

    def delete(self, table_name: str, id_to_delete, id_name):
        key = _form_key(id_to_delete, id_name)
        table: dict = self.dynamo_db.get(table_name)
        del table[key]


def _get_key(table_name: str, item: dict):
    if table_name == BREWS_DYNAMO_TABLE:
        return item[BREW_TABLE_ID]
    elif table_name == MEASUREMENT_SERIES_DYNAMO_TABLE:
        return item["brew_remote_id"] + item["source_name"]


def _form_key(id_to_get, id_name):
    if type(id_to_get) == list:
        key = ""
        for id_single in id_to_get:
            key = key + id_single
        return key
    else:
        return id_to_get
