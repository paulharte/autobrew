import datetime

from storage.serializable import Serializable


class StageDetailsRemote(Serializable):
    def __init__(self):
        self.start_time: datetime.datetime
        self.stage_name: str
        self.estimated_end_time: datetime.datetime