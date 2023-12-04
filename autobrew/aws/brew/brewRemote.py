import datetime
from typing import List

from brew.stageDetailsRemote import StageDetailsRemote
from storage.serializable import Serializable


class BrewRemote(Serializable):
    def __init__(self):
        self.id: str
        self.name: str
        self.active: bool
        self.measurement_ids: List[str]
        self.remote_id: str
        self.start_time: datetime.datetime
        self.description: str
        self.stages: List[StageDetailsRemote]

    @property
    def current_stage(self) -> StageDetailsRemote:
        if self.stages:
            return self.stages[-1]

    def mandatory_attributes(self) -> dict:
        return {"name": str, "active": bool, "remote_id": str}

    @classmethod
    def from_dict(cls, attributes: dict):
        obj = Serializable.from_dict(attributes)
        obj.__class__ = cls
        stages = attributes.get("stages") or []
        obj.stages = [StageDetailsRemote.from_dict(stage) for stage in stages]
        obj.validate()
        return obj

    def to_dict(self):
        d = super().to_dict()
        d["stages"] = [stage.to_dict() for stage in self.stages]
        return d
