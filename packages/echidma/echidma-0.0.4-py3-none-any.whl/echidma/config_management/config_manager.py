import yaml, os
import numpy as np
from copy import deepcopy

class ConfigManager:
    def __init__(self, config=None, config_file=None):

        if config is None:
            if config_file is None:
                raise ValueError("You have given neither a config dictionary nor a configuration filename.")
            else:
                with open(config_file, 'r') as file:
                    self.config = yaml.safe_load(file)
        elif isinstance(config, ConfigManager):
            self.config = deepcopy(config.config)
        else:
            self.config = config


        self.filenames = self.config['filenames']

        if 'data_shapes' in self.config:
            self.data_shapes = self.config['data_shapes']
        else:
            self.data_shapes = [None for filename in self.filenames]


        if 'decompressed_data_shape' in self.config:
            self.decompressed_data_shape = self.config['decompressed_data_shape']
        else:
            self.decompressed_data_shape = (sum([shape[0] for shape in self.data_shapes]), *self.data_shapes[0][1:])


        if 'dataset_name' in self.config:
            self.dataset_name = self.config['dataset_name']
        else:
            self.dataset_name = 'data'
        

        self.param_to_index = {}
        self.input_axes = []

        if 'axes' in self.config:
            for param_idx, (param, axis) in enumerate(self.config['axes'].items()):
                self.input_axes.append(np.array(axis))
                self.param_to_index[param] = param_idx



        if 'parameter_ranges' in self.config:
            self.parameter_ranges = self.config['parameter_ranges']
        else:
            self.parameter_ranges = None



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
    
    @classmethod
    def create_filename(file_id=None, filestem=None, ext='npy'):

        rel_filename_str = f"{filestem}_{file_id}.{ext}"

        working_dir = os.getcwd()

        absolute_file_str = f"{working_dir}/{rel_filename_str}"

        return rel_filename_str, absolute_file_str
    

    @classmethod
    def find_and_create_from_cfg(cls, file_stem, directory=None, **kwargs):
        """Recursively find .cfg files with the given file stem and create an instance of ConfigManager."""
        
        
        if directory is None:
            directory = os.getcwd()
        
        config_data = {'filenames': [], 'decompressed_matrix_shape': None, 'data_shapes':[]}
        config_data.update(kwargs)
        
        for root, dirs, files in os.walk(directory):
            for file in files:

                if file.startswith(file_stem) and file.endswith('.cfg'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as cfg_file:
                        cfg_data = yaml.safe_load(cfg_file)
                        config_data['filenames'].extend(cfg_data.get('filenames', []))
                        config_data['data_shapes'].extend(cfg_data.get('data_shapes', []))
        
        shapes = config_data['data_shapes']

        config_data['data_shapes'] = [(*shape,) for shape in shapes]

        return cls(config=config_data)
    

    @classmethod
    def find_and_create_from_file_ext(cls, file_stem, directory=None, ext='npy', **kwargs):


        if directory is None:
            directory = os.getcwd()
        
        config_data = {'filenames': [], 
                       'decompressed_matrix_shape': None, 'data_shapes':[]}
        config_data.update(kwargs)

        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.startswith(file_stem) and file.endswith(ext):
                    relative_path = os.path.relpath(os.path.join(root, file), directory)
                    config_data['filenames'].append(relative_path)
        
        return cls(config=config_data)


        


    
    

