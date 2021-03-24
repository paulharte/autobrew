import datetime

from injector import inject

from autobrew.sync.identityManger import IdentityManager


class CachedIdentityManger(object):
    CACHE_LIFE_SECONDS = 60

    @inject
    def __init__(self, identity_manager: IdentityManager):
        self.identityManager = identity_manager
        self.cached_token = None
        self.cached_time = datetime.datetime.utcnow()

    def get_access_token(self) -> str:
        if self.cached_token and not self.is_expired():
            return self.cached_token
        else:
            new_token = self.identityManager.get_access_token()
            self.cached_token = new_token
            self.cached_time = datetime.datetime.utcnow()

    def is_expired(self):
        now = datetime.datetime.utcnow()
        age = now - self.cached_time
        return age.seconds > self.CACHE_LIFE_SECONDS
