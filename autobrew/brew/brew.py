import datetime
from typing import List

from autobrew.aws.storage.serializable import Serializable
from autobrew.brew.stageDetails import StageDetails
from autobrew.brew.stages import Stage


class Brew(Serializable):
    def __init__(self, name: str, start_time: datetime.datetime):
        self.name = name
        self.id: str
        self.measurement_ids: List[str]
        self.active = False
        self.start_time = start_time
        self.remote_id: str
        self.description: str
        self.current_stage = Stage.FERMENTING  # DEPRECATED
        self.stages: List = [StageDetails(start_time, Stage.FERMENTING)]

    def get_display_name(self) -> str:
        return self.name if self.name else self.id

    def get_name(self):
        return self.name

    def get_current_stage_details(self) -> StageDetails:
        if self.stages:
            return self.stages[-1]

    def start_new_stage(self, stage_name: Stage, stage_start_time: datetime.datetime):
        new_stage = StageDetails(stage_start_time, stage_name)
        self.stages.append(new_stage)

    def complete(self, time: datetime.datetime):
        self.start_new_stage(Stage.COMPLETE, time)

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
