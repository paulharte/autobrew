APP_LOGIN = "cognito-app-login"


class IdentitySecrets(object):
    def __init__(self, env: str,  secrets: dict):
        self.secrets = secrets
        self.env = env

    def _extract_value(self, key1: str, key2: str) -> str:
        try:
            return self.secrets[key1][self.env][key2]
        except KeyError:
            raise RuntimeError("Missing value in secrets file: %s:%s" % (key1, key2))

    def get_client_id(self):
        return self._extract_value(APP_LOGIN, "app-client-id")

    def get_client_secret(self):
        return self._extract_value(APP_LOGIN, "app-client-secret")
