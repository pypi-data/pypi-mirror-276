import yaml
import numpy as np

class ConfigManager:
    def __init__(self, config=None, config_file=None):

        if config is None:
            if config_file is None:
                raise ValueError("You have given neither a config dictionary nor a configuration filename.")
            else:
                with open(config_file, 'r') as file:
                    self.config = yaml.safe_load(file)
        else:
            self.config = config


        self.filenames = self.config['filenames']

        if 'dataset_name' in self.config:
            self.dataset_name = self.config['dataset_name']
        else:
            self.dataset_name = 'data'
        

        self.param_to_index = {}
        self.input_axes = []

        for param_idx, (param, axis) in enumerate(self.config['axes'].items()):

            self.input_axes.append(np.array(axis))

            self.param_to_index[param] = param_idx


        if 'parameter_ranges' in self.config:
            self.parameter_ranges = self.config['parameter_ranges']
        else:
            self.parameter_ranges = None

        if 'decompressed_data_shape' in self.config:
            self.decompressed_data_shape = self.config['decompressed_data_shape']
        else:
            self.decompressed_data_shape = [np.nan]


    def __call__(self, values):
        slices = tuple(slice(None) if value is None else axis[np.abs(axis - value).argmin()]
                       for axis, value in zip(self.input_axes, values))
        
        return slices, self.filenames
    

    
    def __iter__(self):
        return iter(self.filenames)
    

    def __getitem__(self, data_slice):

        return self.filenames[data_slice]
    
    @property
    def shape(self):
        return self.decompressed_data_shape
    

