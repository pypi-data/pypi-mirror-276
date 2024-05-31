import numpy as np
import h5py as hp
from echidma.indexer_base import EchidmaBase


class EchidmaH5(EchidmaBase):
    def __init__(self, config=None, config_file=None, cache_size=5):
        super().__init__(config=config, config_file=config_file, cache_size=cache_size)
            

    
    def load_chunk(self, filename, data_slice):

        with hp.File(filename, 'r', libver='latest', swmr=True, ) as f:
            dset = f[self.config_manager.dataset_name]
            chunk = dset[data_slice]

        return chunk




