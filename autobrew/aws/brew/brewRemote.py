import datetime
from typing import List
from autobrew.aws.storage.serializable import Serializable


class BrewRemote(Serializable):
    def __init__(self):
        self.id: str
        self.name: str
        self.active: bool
        self.measurement_ids: List[str]
        self.remote_id: str
        self.start_time: datetime.datetime
