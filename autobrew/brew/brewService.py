from typing import List

from injector import inject

from autobrew.brew.brew import Brew
from autobrew.brew.brewStorage import BrewStorage


class BrewService(object):
    @inject
    def __init__(self, storage: BrewStorage):
        self.storage = storage

    def new(self, name) -> Brew:
        brew = Brew(name)
        brew.active = True
        brew.id = self.storage.generate_id()
        brew.remote_id = self.storage.generate_remote_id()
        brew = self.storage.save(brew)
        self._set_others_inactive(brew.id)
        return brew

    def save(self, brew: Brew):
        return self.storage.save(brew)

    def get_all(self) -> List[Brew]:
        return self.storage.get_all()

    def get_active(self) -> Brew:
        for brew in self.get_all():
            if brew.active:
                return brew

    def _set_others_inactive(self, active_id: int):
        for brew in self.get_all():
            if brew.active and (brew.id != active_id):
                brew.active = False
                self.save(brew)

    def set_active(self, brew_id: int) -> Brew:
        brew = self.storage.read(brew_id)
        brew.active = True
        brew = self.storage.save(brew)
        self._set_others_inactive(brew.id)
        return brew
