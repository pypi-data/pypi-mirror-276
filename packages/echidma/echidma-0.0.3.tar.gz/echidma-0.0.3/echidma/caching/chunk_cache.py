from collections import OrderedDict




class ChunkCache:
    def __init__(self, max_size):
        self.max_size = max_size
        self.cache = OrderedDict()

    def get(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return None

    def put(self, key, value):
        self.cache[key] = value
        if len(self.cache) > self.max_size:
            self.cache.popitem(last=False)
