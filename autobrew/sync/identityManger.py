import json
import logging
import os

import requests

import yaml
from injector import inject

from autobrew.brew_settings import ROOT_DIR, APP_LOGGING_NAME
from autobrew.sync.awsConfig import AwsConfig
from autobrew.sync.exceptions import SyncFailedError
from autobrew.sync.identitySecrets import IdentitySecrets

logger = logging.getLogger(APP_LOGGING_NAME)


class IdentityManager(object):
    @inject
    def __init__(self, config: AwsConfig):
        self.config = config

    def _extract_secrets(self) -> IdentitySecrets:
        path = os.path.join(ROOT_DIR, "secrets.yaml")
        try:
            with open(path) as file:
                return IdentitySecrets(self.config.env, yaml.safe_load(file))
        except FileNotFoundError:
            msg = (
                "Please create a secrets.yaml file in the base of this project (%s)"
                % path
            )
            raise RuntimeError(msg)

    def get_access_token(self) -> str:
        secrets = self._extract_secrets()

        body = {
            "grant_type": "client_credentials",
            "client_id": secrets.get_client_id(),
            "client_secret": secrets.get_client_secret(),
            "scope": self._determine_scope(),
        }
        url = self.config.get_token_endpoint()
        response = requests.post(url, data=body)
        if response.status_code != 200:
            logger.warning("failed post to %s(%s)", url, response.status_code)
            raise SyncFailedError(response.text)
        return json.loads(response.text)["access_token"]

    def _determine_scope(self):
        return self.config.get_base_url() + "brews.readwrite"
