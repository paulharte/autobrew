
class AbstractSource(object):
    nickname = None
    is_primary = False

    def __init__(self):
        self.is_primary = False

    def set_nickname(self, name: str):
        self.nickname = name

    def set_primary(self, is_primary):
        self.is_primary = is_primary

    def get_name(self):
        pass

    def get_display_name(self):
        if self.nickname:
            return self.nickname
        else:
            return self.get_name()
