import datetime
from typing import List

from storage.serializable import Serializable


class Brew(Serializable):
    def __init__(self, name: str, start_time: datetime.datetime):
        self.name = name
        self.id: int
        self.measurement_ids: List[str]
        self.active = False
        self.start_time = start_time
        self.remote_id:str


    def get_display_name(self) -> str:
        return self.name if self.name else self.id

    def get_name(self):
        return self.name

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return "Brew Name:%s, Id:%s" % (self.name, self.id)


def sort_brews(brews: List[Brew]) -> List[Brew]:
    # sorts with active on top
    return sorted(brews, key=lambda br: int(br.active) + (br.start_time.toordinal() * 1/ 100000000), reverse=True)
