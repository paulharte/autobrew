import os
import yaml


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
        return self._extract_value("consumer", "key")

    def get_consumer_secret(self):
        return self._extract_value("consumer", "secret")

    def get_access_token_key(self):
        return self._extract_value("access-token", "key")

    def get_access_token_secret(self):
        return self._extract_value("access-token", "secret")


class TwitterSecretException(RuntimeError):
    def __init__(self, msg):
        msg = msg + " Example YAML file: " + EXAMPLE_SECRET_YAML
        super().__init__(msg)


def extract_secrets() -> TwitterSecrets:
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "../../twitter_secrets.yaml")
    try:
        with open(path) as file:
            secrets_dict = yaml.safe_load(file)
            return TwitterSecrets(secrets_dict)
    except FileNotFoundError:
        msg = (
            "Please create a twitter_secrets.yaml file in the base of this project (%s)"
            % path
        )
        raise TwitterSecretException(msg)


EXAMPLE_SECRET_YAML = """
consumer:
  key: XXXX
  secret: XXXX
access-token:
  key: XXX
  secret: XXX"""
