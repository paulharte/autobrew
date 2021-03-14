from typing import List


class Brew(object):
    def __init__(self, name: str):
        self.name = name
        self.id: int
        self.measurement_ids: List[str]
        self.active = False
        self.remote_id: str

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
    return sorted(brews, key=lambda br: int(br.active), reverse=True)
