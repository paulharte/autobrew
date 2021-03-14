import uuid
from typing import List

import logging
from injector import inject

from autobrew.brew.brew import Brew
from autobrew.brew.brewExceptions import AutobrewNotFoundError
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

    def read(self, brew_id: int) -> Brew:
        return self.file_storage.read(str(brew_id), self.SUB_FOLDER)

    def get_all(self) -> List[Brew]:
        brews = []
        for brew_id in self.file_storage.get_storage_files(None, self.SUB_FOLDER):
            try:
                brews.append(self.read(brew_id))
            except AutobrewNotFoundError as e:
                logger.error(e)
        return brews

    def generate_id(self) -> int:
        for i in range(100000):
            if str(i) not in self.file_storage.get_storage_files(None, self.SUB_FOLDER):
                return i
        raise RuntimeError("Unable to get id for new brew")

    def generate_remote_id(self) -> str:
        return str(uuid.uuid4())
