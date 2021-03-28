import datetime
from typing import List
from storage.serializable import Serializable


class BrewRemote(Serializable):
    def __init__(self):
        self.id: str
        self.name: str
        self.active: bool
        self.measurement_ids: List[str]
        self.remote_id: str
        self.start_time: datetime.datetime
        self.current_stage: str
        self.description: str

    def mandatory_attributes(self) -> dict:
        return {"name": str, "active": bool, "remote_id": str, "current_stage": str}
