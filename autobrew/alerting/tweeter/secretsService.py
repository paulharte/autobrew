import os
import yaml

from autobrew.brew_settings import ROOT_DIR

CONSUMER = "twitter-consumer"
ACCCESS_TOKEN = "twitter-access-token"
EXAMPLE_SECRET_YAML = """
%s:
  key: XXXX
  secret: XXXX
%s:
  key: XXX
  secret: XXX""" % (
    CONSUMER,
    ACCCESS_TOKEN,
)


class TwitterSecrets(object):
    def __init__(self, secrets: dict):
        self.secrets = secrets

    def _extract_value(self, key1: str, key2: str) -> str:
        try:
            return self.secrets[key1][key2]
        except KeyError:
            raise TwitterSecretException(
                "Missing value in secrets file: %s:%s" % (key1, key2)
            )

    def get_consumer_key(self):
        return self._extract_value(CONSUMER, "key")

    def get_consumer_secret(self):
        return self._extract_value(CONSUMER, "secret")

    def get_access_token_key(self):
        return self._extract_value(ACCCESS_TOKEN, "key")

    def get_access_token_secret(self):
        return self._extract_value(ACCCESS_TOKEN, "secret")


class TwitterSecretException(RuntimeError):
    def __init__(self, msg):
        msg = msg + " Example YAML file: " + EXAMPLE_SECRET_YAML
        super().__init__(msg)


def extract_secrets() -> TwitterSecrets:
    path = os.path.join(ROOT_DIR, "secrets.yaml")
    try:
        with open(path) as file:
            secrets_dict = yaml.safe_load(file)
            return TwitterSecrets(secrets_dict)
    except FileNotFoundError:
        msg = (
            "Please create a secrets.yaml file in the base of this project (%s)" % path
        )
        raise TwitterSecretException(msg)
