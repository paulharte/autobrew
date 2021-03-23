from injector import inject

from autobrew.brew.brew import Brew
from autobrew.brew_settings import APP_LOGGING_NAME
from autobrew.measurement.measurementSeries import MeasurementSeries
from autobrew.sync.remoteSync import RemoteSync
import logging

logger=logging.getLogger(APP_LOGGING_NAME)

class SyncService(object):
    @inject
    def __init__(self, remote_sync: RemoteSync):
        self.remote_sync = remote_sync


    def sync_brew(self, brew: Brew):
        self.remote_sync.sync_brew(brew)
        logger.info("Brew %s synced to cloud" % brew.remote_id)


    def sync_measurements(self, brew: Brew, series: MeasurementSeries):
        self.remote_sync.sync_measurements(brew, series)
        logger.info("Measurement on %s for brew %s synced to cloud" % (series.source_name, brew.remote_id))