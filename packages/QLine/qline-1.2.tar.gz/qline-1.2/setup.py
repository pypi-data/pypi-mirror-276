import setuptools
from setuptools import setup, find_packages

with open("README.md", "r") as f:
    ldescription = f.read()

setuptools.setup(
    include_package_data = True,
    name         = 'QLine',
    version      = '1.2',
    description  = 'For the calculation of one-dimensional Schroedinger equations',
    author       = 'Michael Welzel',
    license      = 'GPLv3',
    package_dir  = {'': 'src/'},
    python_requires = '>=3.11.4',
    install_requires = ['numpy>=1.24.2','matplotlib>=3.7.0', 'scipy>=1.10.1'],
    classifiers  = ["Programming Language :: Python :: 3",
                    "Operating System :: OS Independent"],
    long_description=ldescription,
    long_description_content_type='text/markdown',  
    keywords=["python", "quantum", "mechanics", "one", "dimensional", "chemistry",
              "harmonic", "oscillator", "basis set method", "variatonal principle"
             ],
    )
