import datetime

from autobrew.aws.storage.serializable import Serializable
from autobrew.brew.stages import Stage


class StageDetails(Serializable):
    def __init__(self, start_time: datetime.datetime, stage_name: Stage):
        self.start_time = start_time
        self.stage_name: Stage = stage_name
        self.estimated_end_time = self.derive_end_time()

    def derive_end_time(self) -> datetime.datetime:
        if self.stage_name == Stage.FERMENTING:
            return self.start_time + datetime.timedelta(days=7)
        if self.stage_name == Stage.BOTTLE_CONDITIONING:
            return self.start_time + datetime.timedelta(days=14)
        else:
            return self.start_time
