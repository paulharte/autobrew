import datetime

from autobrew.brew.brewService import BrewService
from autobrew.brew.stages import Stage
from autobrew.sync.syncService import SyncService


def migrate_brews(brew_service: BrewService, sync: SyncService):
    brews = brew_service.get_all()
    now = datetime.datetime.utcnow()
    for brew in brews:
        if not brew.stages:
            brew.start_new_stage(Stage.FERMENTING, brew.start_time)
            if brew.start_time + datetime.timedelta(days=21) < now:
                brew.start_new_stage(Stage.BOTTLE_CONDITIONING, brew.start_time + datetime.timedelta(days=7))
                brew.complete(brew.start_time + datetime.timedelta(days=21))
            try:
                del brew.__dict__['current_stage']
            except KeyError:
                pass
            brew_service.save(brew)
            sync.sync_brew(brew)

    print('Migration complete!')

