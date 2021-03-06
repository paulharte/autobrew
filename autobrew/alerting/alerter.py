from injector import inject, singleton

from autobrew.alerting.tweeter.twitterAlerts import TwitterAlerter
from autobrew.brew_settings import TWITTER_USER_TO_ALERT


class Alerter(object):
    @singleton
    @inject
    def __init__(self, twitter_alerter: TwitterAlerter):
        self.twitter_alerter = twitter_alerter

    def alert_owner(self, msg: str):
        self.twitter_alerter.send_dm(TWITTER_USER_TO_ALERT, msg)

    def public_message(self, msg: str):
        self.twitter_alerter.tweet(msg)
