from time import time


class Cache:
    def __init__(self, initiator: type = dict, initiator_data: dict or list = None):
        self.initiator = initiator
        self.initiator_data = initiator_data
        self.__init_cache()
        self.updated = time()

    def __init_cache(self):
        self.cache = self.initiator(self.initiator_data) if self.initiator_data is not None else self.initiator()

    def _set(self, key, value):
        self.cache[key] = value
        self.updated = time()

    def _get(self, key):
        return self.cache[key]

    def __setitem__(self, key, value):
        self._set(key, value)

    def __getitem__(self, key):
        return self._get(key)

    def clear(self):
        self.__init_cache()
        self.updated = time()

    def clear_expired(self, expiration_time: int):
        if self.updated + expiration_time < time():
            self.clear()
