import os
import pickle
from typing import List


FOLDER_NAME = "storage"
FOLDER_PATH = os.path.dirname(os.path.abspath(__file__)).replace("file", FOLDER_NAME)


class FileStorage(object):
    """ Handles all file io"""

    def read(self, filename: str, sub_folder: str = None):
        path = self.form_path(filename, sub_folder)
        # Potentially throws FileNotFoundError, EOFError
        with open(path, "rb") as file:
            return pickle.load(file)

    def save(self, filename: str, obj, sub_folder: str = None):
        path = self.form_path(filename, sub_folder)
        with open(path, "wb") as file:
            pickle.dump(obj, file)

    def form_path(self, filename: str, sub_folder: str):
        if sub_folder:
            return FOLDER_PATH + "/" + sub_folder + "/" + filename
        else:
            return FOLDER_PATH + "/" + filename

    def get_storage_files(
        self, suffix: str = None, sub_folder: str = None
    ) -> List[str]:
        """ Returns just filenames, not paths"""
        folder = os.path.join(FOLDER_PATH, sub_folder) if sub_folder else FOLDER_PATH
        try:
            files = os.listdir(folder)
        except FileNotFoundError:
            os.mkdir(folder)
            files = os.listdir(folder)
        if suffix:
            return filter(lambda x: x.endswith(suffix), files)
        else:
            return files
