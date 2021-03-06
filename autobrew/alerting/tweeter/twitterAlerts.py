import logging

import twitter

from autobrew.alerting.tweeter.secrets import TwitterSecrets
from autobrew.brew_settings import APP_LOGGING_NAME

logger = logging.getLogger(APP_LOGGING_NAME)


class TwitterAlerter(object):
    def __init__(self, secret: TwitterSecrets):
        self.api = twitter.Api(
            consumer_key=secret.get_consumer_key(),
            consumer_secret=secret.get_consumer_secret(),
            access_token_key=secret.get_access_token_key(),
            access_token_secret=secret.get_access_token_secret(),
        )

    def tweet(self, text: str):
        self.api.PostUpdate(text)

    def send_dm(self, receiving_user_handle: str, msg: str):
        if receiving_user_handle.startswith("@"):
            receiving_user_handle = receiving_user_handle[1:]
        receiving_user = self.api.GetUser(
            screen_name=receiving_user_handle, include_entities=False
        )
        resp = self.api.PostDirectMessage(
            text=msg, user_id=receiving_user.id, return_json=True
        )
        logger.info("Twitter alert sent: %s" % resp)
