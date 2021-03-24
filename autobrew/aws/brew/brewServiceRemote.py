import os
from typing import List

import uuid
from brew.brewRemote import BrewRemote
from storage.dynamo import Dynamo

BREWS_DYNAMO_TABLE = os.environ.get("brew_table", default="autobrew_brews")
BREW_TABLE_ID = "remote_id"


class BrewServiceRemote(object):
    def __init__(self, dynamo: Dynamo):
        self.db = dynamo

    def getAll(self) -> List[BrewRemote]:
        return [
            BrewRemote.from_dict(json_brew)
            for json_brew in self.db.get_all(BREWS_DYNAMO_TABLE)
        ]

    def put(self, brew: BrewRemote):
        self.db.put(BREWS_DYNAMO_TABLE, brew.to_dict())

    def get(self, id_to_get: int) -> BrewRemote:
        brew_dict = self.db.get(BREWS_DYNAMO_TABLE, str(id_to_get), BREW_TABLE_ID)
        if brew_dict:
            return BrewRemote.from_dict(brew_dict)
        else:
            return None

    def create(self, brew: BrewRemote):
        self.put(brew)

    def delete(self, id_to_delete: int):
        self.db.delete(BREWS_DYNAMO_TABLE, str(id_to_delete), BREW_TABLE_ID)

    def get_unique_brew_id(self) -> str:
        return uuid.uuid4()


def make_brew_service() -> BrewServiceRemote:
    return BrewServiceRemote(Dynamo())
