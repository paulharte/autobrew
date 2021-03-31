import datetime
from typing import List

from autobrew.aws.storage.serializable import Serializable
from autobrew.aws.brew.stages import FERMENTING
from autobrew.brew.stages import Stage


class Brew(Serializable):
    def __init__(self, name: str, start_time: datetime.datetime):
        self.name = name
        self.id: str
        self.measurement_ids: List[str]
        self.active = False
        self.start_time = start_time
        self.remote_id: str
        self.current_stage: Stage = Stage.FERMENTING
        self.description: str

    def get_display_name(self) -> str:
        return self.name if self.name else self.id

    def get_name(self):
        return self.name

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return "Brew '%s'(Id:%s, RemoteId:%s)" % (self.name, self.id, self.remote_id)


def sort_brews(brews: List[Brew]) -> List[Brew]:
    # sorts with active on top
    return sorted(
        brews,
        key=lambda br: int(br.active) + (br.start_time.toordinal() * 1 / 100000000),
        reverse=True,
    )
