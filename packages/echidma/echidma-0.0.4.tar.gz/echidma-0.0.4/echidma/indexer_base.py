import numpy as np
import h5py as hp
from echidma.config_management import ConfigManager
from echidma.caching import ChunkCache


class EchidmaBase:
    def __init__(self, config=None, config_file=None, cache_size=5):

        self.config_manager = ConfigManager(config, config_file)

        self.cache = ChunkCache(cache_size)


    
    def get_chunk_by_slice(self, filename, data_slice):


        # This is a base class for more specific methods to access data from disc
            # that should/will have there specific implementation of "load_chunk" 
        chunk = self.load_chunk(filename, data_slice)
        
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

        data = [self.get_chunk_by_slice(filename, data_slice) for filename in self.config_manager]

        data = np.concatenate(data,axis=axis)

        self.cache.put(cache_key, data)

        return data



    def __getitem__(self, data_slice):

        return self.get_and_combine_chunks(data_slice=data_slice)
    

        
    def __call__(self, *args, **kwargs):

        data_slice = self.config_manager(*args, **kwargs)

        return self[data_slice]
    

    @property
    def shape(self):
        return self.config_manager.shape

    

    @classmethod
    def save_to_file(cls, parameter_data, data, config=None, config_file=None, filename = None, **kwargs):

        if not('compression' in kwargs):
            kwargs['compression' ] = 'lzf'
            

        config_manager = ConfigManager(config, config_file)

        if filename is None:
            filename = config_manager.param_to_filename(parameter_data)

        with hp.File(filename, 'w') as f:

            dset = f.create_dataset(config_manager.dataset_name, 
                                    data=data, 
                                    **kwargs)
        

    def __add__(self, other):
        return self[:] + other
    

    def __radd__(self, other):
        return self[:] + other




