import os
import pickle
from typing import List


FOLDER_NAME = "storage"
FOLDER_PATH = os.path.dirname(os.path.abspath(__file__)).replace(
    "measurement", FOLDER_NAME
)


class FileStorage(object):
    """ Handles all file io"""

    def read(self, filename: str):
        # Potentially throws FileNotFoundError, EOFError
        with open(FOLDER_PATH + "/" + filename, "rb") as file:
            return pickle.load(file)

    def save(self, filename: str, obj):
        with open(FOLDER_PATH + "/" + filename, "wb") as file:
            pickle.dump(obj, file)

    def get_storage_files(self, suffix: str = None) -> List[str]:
        files = os.listdir(FOLDER_PATH)
        if suffix:
            return filter(lambda x: x.endswith(self.SUFFIX), files)
        else:
            return files
