import logging

from injector import inject, singleton

from autobrew.alerting.tweeter.twitterAlerts import TwitterAlerter
from autobrew.brew_settings import TWITTER_USER_TO_ALERT, APP_LOGGING_NAME

logger = logging.getLogger(APP_LOGGING_NAME)


class Alerter(object):
    @singleton
    @inject
    def __init__(self, twitter_alerter: TwitterAlerter):
        self.twitter_alerter = twitter_alerter

    def alert_owner(self, msg: str):
        self.twitter_alerter.send_dm(TWITTER_USER_TO_ALERT, msg)

    def public_message(self, msg: str):
        if len(msg) > 240:
            msg = msg[0:239]
        try:
            self.twitter_alerter.tweet(msg)
        except Exception as e:
            msg = "Exception sending public message: %s" % e
            logger.error(msg)
            logger.exception(e)
            self.alert_owner(msg)
