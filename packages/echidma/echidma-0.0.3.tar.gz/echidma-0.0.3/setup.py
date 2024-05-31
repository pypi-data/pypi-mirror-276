from setuptools import setup, find_packages
import subprocess
import sys
import os
import time

setup(name='echidma',
      description='Embarrassingly Chunky Hard Indexed Data Memory Access',
      url='https://github.com/lpin0002/ECHIDMA',
      author='Liam Pinchbeck',
      author_email='Liam.Pinchbeck@monash.edu',
      license="MIT",
      version='0.0.3',
      packages=find_packages(),

      # For a lot of the DM spectral classes we require that dict types are ordered
      python_requires='>=3.6',
      install_requires=["scipy==1.11.3",
                        "tqdm>=4.65.0",
                        "numpy>=1.23",
                        "pandas>=1.5.3",
                        "pytest",
                        "h5py",
                        "hdf5plugin",
                        "numcodecs",],

      classifiers=[
          "License :: OSI Approved :: MIT License",
          "Operating System :: Unix",],
      )
