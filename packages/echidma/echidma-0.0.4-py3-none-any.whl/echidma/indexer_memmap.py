import numpy as np
from echidma.indexer_base import EchidmaBase
from echidma.config_management import ConfigManager


class EchidmaMemMap(EchidmaBase):
    def __init__(self, config=None, config_file=None, cache_size=5):
        super().__init__(config=config, config_file=config_file, cache_size=cache_size)
        
        
        self.array = np.memmap(
            self.config_manager.filenames[0], 
            mode='r+', 
            shape=self.config_manager.decompressed_data_shape,
            dtype=np.float64)
        
        self.arrays = {}

        offset = 0

        for file_idx, (filename, datashape) in enumerate(zip(self.config_manager.filenames, self.config_manager.data_shapes)):

            self.arrays[filename] = np.memmap(filename, mode='r', shape=datashape, dtype=np.float64)

            chunk = datashape[0]
            if filename!=self.config_manager.filenames[0]:
                self.array[offset:offset+chunk, ...] = self.arrays[filename]

            offset+=chunk





        

    
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

        data = self.array[data_slice]

        self.cache.put(cache_key, data)

        return data
    
    def create_filename(file_id=None, filestem=None, ext='npy'):

        return ConfigManager.create_filename(file_id=file_id, filestem=filestem, ext=ext)