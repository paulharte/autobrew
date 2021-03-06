import logging

from autobrew.brew_settings import APP_LOGGING_NAME

logger = logging.getLogger(APP_LOGGING_NAME)


class StubTwitterAlerter(object):
    def tweet(self, text: str):
        logger.info("MockTweet: %s" % text)

    def send_dm(self, receiving_user_handle: str, msg: str):
        logger.info("MockTweetDM to %s: %s" % (receiving_user_handle, msg))
