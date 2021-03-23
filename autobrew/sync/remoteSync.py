from injector import inject

from autobrew.brew.brew import Brew
from autobrew.measurement.measurementSeries import MeasurementSeries
from autobrew.sync.awsConfig import AwsConfig
from autobrew.sync.identityManger import IdentityManager
import requests


class RemoteSync(object):
    BREW_ENDPOINT = 'brew/'

    @inject
    def __init__(self, identity_manager: IdentityManager, config: AwsConfig):
        self.identity_manager = identity_manager
        self.config = config

    def sync_brew(self, brew: Brew):
        token = self.identity_manager.get_access_token()
        url = self.formBrewUrl(brew.remote_id)
        resp = requests.put(url, brew.to_json(), headers = _form_headers(token))

    def sync_measurements(self, brew: Brew,  series: MeasurementSeries):
        token = self.identity_manager.get_access_token()
        ##/ brew / {brew_remote_id} / measurements / {source_name}
        url = self.formMeasurementUrl(brew.remote_id, series.source_name)
        resp = requests.put(url, series.to_json(), headers=_form_headers(token))

    def formMeasurementUrl(self, brew_remote_id:str,  series_source :str):
        return self.config.get_base_url() + self.BREW_ENDPOINT + brew_remote_id + '/measurements/' + series_source

    def formBrewUrl(self, brew_remote_id:str):
        return self.config.get_base_url() + self.BREW_ENDPOINT + brew_remote_id


def _form_headers(token: str) -> dict:
    return {'Authorization': 'bearer %' % token}


