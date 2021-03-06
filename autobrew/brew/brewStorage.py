from typing import List

import logging
from injector import inject

from autobrew.brew.brew import Brew
from autobrew.brew_settings import APP_LOGGING_NAME
from autobrew.file.fileStorage import FileStorage

logger = logging.getLogger(APP_LOGGING_NAME)


class BrewStorage(object):
    SUB_FOLDER = "brews"

    @inject
    def __init__(self, file_storage: FileStorage):
        self.file_storage = file_storage

    def save(self, brew: Brew) -> Brew:
        self.file_storage.save(str(brew.id), brew, self.SUB_FOLDER)
        return brew

    def new(self, brew: Brew) -> Brew:
        brew_id = self._find_unused_id()
        brew.id = brew_id
        return self.save(brew)

    def read(self, brew_id: int) -> Brew:
        return self.file_storage.read(str(brew_id), self.SUB_FOLDER)

    def get_all(self) -> List[Brew]:
        brews = []
        for brew_id in self.file_storage.get_storage_files(None, self.SUB_FOLDER):
            try:
                brews.append(self.read(brew_id))
            except (FileNotFoundError, EOFError) as e:
                logger.error(e)
        return brews

    def _find_unused_id(self) -> int:
        for i in range(100000):
            if str(i) not in self.file_storage.get_storage_files(None, self.SUB_FOLDER):
                return i
        raise RuntimeError("Unable to get id for new brew")
