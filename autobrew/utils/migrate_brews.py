import datetime

from autobrew.brew.brewService import BrewService
from autobrew.brew.stages import Stage
from autobrew.measurement.measurementService import MeasurementService
from autobrew.sync.syncService import SyncService


def migrate_brews(brew_service: BrewService, sync: SyncService, measurement_service: MeasurementService):
    brews = brew_service.get_all()
    now = datetime.datetime.utcnow()
    for brew in brews:
        if not hasattr(brew, 'stages'):
            brew.stages = []
            brew.start_new_stage(Stage.FERMENTING, brew.start_time)
            brew.start_new_stage(Stage.BOTTLE_CONDITIONING, brew.start_time + datetime.timedelta(days=7))
            if brew.start_time + datetime.timedelta(days=21) < now:
                brew.complete(brew.start_time + datetime.timedelta(days=21))
            try:
                del brew.__dict__['current_stage']
            except KeyError:
                pass
            brew_service.save(brew)
            sync.sync_brew(brew)

        for series in measurement_service.get_all_series_for_brew(brew):
            if not hasattr(series, 'brew_remote_id'):
                series.brew_remote_id = brew.remote_id
                measurement_service.save_series(series)

    print('Migration complete!')

