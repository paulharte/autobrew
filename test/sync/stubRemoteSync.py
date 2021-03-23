from autobrew.brew.brew import Brew
from autobrew.measurement.measurementSeries import MeasurementSeries


class StubRemoteSync(object):

    def sync_brew(self, brew: Brew):
        pass

    def sync_measurements(self, brew: Brew,  series: MeasurementSeries):
        pass