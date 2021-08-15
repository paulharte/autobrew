import datetime
from typing import List

from injector import inject

from autobrew.alerting.alerter import Alerter
from autobrew.brew.brew import Brew
from autobrew.brew.brewStorage import BrewStorage
from autobrew.brew.stages import Stage
from autobrew.sync.syncService import SyncService


class BrewService(object):
    @inject
    def __init__(self, storage: BrewStorage, sync: SyncService, alerter: Alerter):
        self.storage = storage
        self.sync = sync
        self.alerter = alerter

    def new(self, name, description: str = None) -> Brew:
        brew = Brew(name, datetime.datetime.utcnow())
        brew.active = True
        brew.id = self.storage.generate_id()
        brew.description = description
        brew.remote_id = self.storage.generate_remote_id()
        brew = self.save(brew)
        self._set_others_inactive(brew.id)
        self.alerter.public_message("A new brew has started:%s autobrew.paulspetprojects.net" % brew.name)
        self._update_stage(brew, Stage.FERMENTING)
        return brew

    def save(self, brew: Brew):
        brew = self.storage.save(brew)
        self.sync.sync_brew(brew)
        return brew

    def get_all(self) -> List[Brew]:
        return self.storage.get_all()

    def get_by_id(self, brew_id) -> Brew:
        return self.storage.read(brew_id)

    def get_active(self) -> Brew:
        for brew in self.get_all():
            if brew.active:
                return brew

    def _set_others_inactive(self, active_id: str):
        for brew in self.get_all():
            if brew.active and (brew.id != active_id):
                brew.active = False
                self.save(brew)

    def set_active(self, brew_id: str) -> Brew:
        brew = self.storage.read(brew_id)
        brew.active = True
        brew = self.save(brew)
        self._set_others_inactive(brew.id)
        return brew

    def set_inactive(self, brew_id: str) -> Brew:
        brew = self.storage.read(brew_id)
        brew.active = False
        return self.save(brew)

    def update_stage(self, brew_id: str, stage: Stage):
        brew = self.get_by_id(brew_id)
        return self._update_stage(brew, stage)

    def _update_stage(self, brew: Brew, stage: Stage):
        brew.start_new_stage(stage, datetime.datetime.utcnow())
        self.alerter.public_message(
            "Brew '%s' has entered stage %s autobrew.paulspetprojects.net" % (brew.name, stage.name))
        return self.save(brew)


    def complete(self, brew_id: str):
        brew = self.get_by_id(brew_id)
        brew.complete(datetime.datetime.utcnow())
        brew.active = False
        return self.save(brew)

