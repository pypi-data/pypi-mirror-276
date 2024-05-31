import numpy as np
from echidma.indexer_base import EchidmaBase


class EchidmaMemMap(EchidmaBase):
    def __init__(self, config=None, config_file=None, cache_size=5):
        super().__init__(config=config, config_file=config_file, cache_size=cache_size)
        
        self.arrays = {}
        for filename in self.config_manager.filenames:
            self.arrays[filename] = np.memmap(filename, shape=self.config_manager.shape, dtype=np.float64)

        
    
    def load_chunk(self, filename, data_slice):

        chunk = self.arrays[filename][data_slice]

        return chunk

    
    def get_and_combine_chunks(self, data_slice, axis=None):


        cache_key = data_slice

        cached_data = self.cache.get(cache_key)
        if cached_data is not None:
            return cached_data


        if axis is None:
            try:
                axis = data_slice.index(slice(None))
            except Exception as err:
                axis = np.newaxis

        data = [self.load_chunk(filename, data_slice) for filename in self.config_manager]

        data = np.concatenate(data,axis=axis)

        self.cache.put(cache_key, data)

        return data