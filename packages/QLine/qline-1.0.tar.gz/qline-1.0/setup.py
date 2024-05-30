import setuptools

setuptools.setup(
      include_package_data = True,
      name         = 'QLine',
      version      = '1.0',
      description  = 'For the calculation of one-dimensional Schroedinger equations',
      author       = 'Michael Welzel',
      license      = 'GPLv3',
      package_dir  = {'': 'src/'},
      python_requires = '>=3.11.4',
      install_requires = ['numpy>=1.24.2','matplotlib>=3.7.0', 'scipy>=1.10.1'],
      classifiers  = ["Programming Language :: Python :: 3",
                      "Operating System :: OS Independent"],
     )


