import logging

from injector import inject

from autobrew.brew.brew import Brew
from autobrew.brew_settings import APP_LOGGING_NAME
from autobrew.measurement.measurementSeries import MeasurementSeries
from autobrew.sync.awsConfig import AwsConfig
from autobrew.sync.cachedIdentityManager import CachedIdentityManger
import requests

from autobrew.sync.exceptions import SyncFailedError

logger = logging.getLogger(APP_LOGGING_NAME)


class RemoteSync(object):
    BREW_ENDPOINT = "brew/"

    @inject
    def __init__(self, identity_manager: CachedIdentityManger, config: AwsConfig):
        self.identity_manager = identity_manager
        self.config = config

    def sync_brew(self, brew: Brew):
        token = self.identity_manager.get_access_token()
        url = self.formBrewUrl(brew.remote_id)
        resp = requests.put(url, brew.to_json(), headers=_form_headers(token))
        if resp.status_code != 200:
            logger.warning("failed put to %s", url)
            raise SyncFailedError(resp.text)

    def sync_measurements(self, brew: Brew, series: MeasurementSeries):
        token = self.identity_manager.get_access_token()
        url = self.formMeasurementUrl(brew.remote_id, series.source_name)
        resp = requests.put(url, series.to_json(), headers=_form_headers(token))
        if resp.status_code != 200:
            logger.warning("failed put to %s", url)
            raise SyncFailedError(resp.text)

    def formMeasurementUrl(self, brew_remote_id: str, series_source: str) -> str:
        return (
            self.config.get_base_url()
            + self.BREW_ENDPOINT
            + brew_remote_id
            + "/measurements/"
            + series_source
        )

    def formBrewUrl(self, brew_remote_id: str) -> str:
        return self.config.get_base_url() + self.BREW_ENDPOINT + brew_remote_id


def _form_headers(token: str) -> dict:
    print("used token")
    print(token)
    return {"Authorization": "Bearer %s" % token}
