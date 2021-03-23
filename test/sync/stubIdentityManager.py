import random


class StubIdentityManager(object):
    def get_access_token(self) -> str:
        return 'randomgeneratedtoken' + str(random.randint(0, 100000))