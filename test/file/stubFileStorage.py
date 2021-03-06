from typing import List


class StubFileStorage(object):
    def __init__(self):
        self._storage = {}

    def read(self, filename: str, sub_folder=None):
        # Potentially throws FileNotFoundError
        key = self._form_key(filename, sub_folder)
        out = self._storage.get(key)
        if out:
            return out
        else:
            raise FileNotFoundError()

    def save(self, filename: str, obj, sub_folder=None):
        key = self._form_key(filename, sub_folder)
        self._storage[key] = obj

    def get_storage_files(
        self, suffix: str = None, sub_folder: str = None
    ) -> List[str]:
        if sub_folder:
            eligible = filter(lambda x: sub_folder in x, list(self._storage.keys()))
            return [self._unform_key(key_text, sub_folder) for key_text in eligible]
        elif suffix:
            return filter(lambda x: suffix in x, list(self._storage.keys()))
        else:
            return list(self._storage.keys())

    def _form_key(self, filename: str, sub_folder: str) -> str:
        return sub_folder + "/" + filename if sub_folder else filename

    def _unform_key(self, key_text: str, sub_folder: str) -> str:
        return key_text.replace(sub_folder + "/", "") if sub_folder else key_text

    def clear_everything(self):
        self._storage = {}
