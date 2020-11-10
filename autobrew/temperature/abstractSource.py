class AbstractSource(object):
    nickname = None
    is_primary = False

    def __init__(self):
        self.is_primary = False

    def set_nickname(self, nick: str):
        self.nickname = nick

    def get_nickname(self) -> str:
        return self.nickname

    def set_primary(self, is_primary):
        self.is_primary = is_primary

    def get_name(self) -> str:
        pass

    def get_display_name(self):
        if self.nickname:
            return self.nickname
        else:
            return self.get_name()
