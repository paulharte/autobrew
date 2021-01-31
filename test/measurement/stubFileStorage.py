from typing import List


class StubFileStorage(object):

    _storage = {}

    def read(self, filename: str):
        # Potentially throws FileNotFoundError
        out = self._storage.get(filename)
        if out:
            return out
        else:
            raise FileNotFoundError()

    def save(self, filename: str, obj):
        self._storage[filename] = obj

    def get_storage_files(self, suffix: str = None) -> List[str]:
        return list(self._storage.keys())
