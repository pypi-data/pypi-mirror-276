# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import os
import warnings
import sys
from distutils.command.install import install

# version string
__version__ = '0.0.1'

# setup attributes
attrs = dict(
    name='dataspanalgorithms',
    version=__version__,
    description='Dummy package for dataspanalgorithms.',
    maintainer='dataspan.ai',
    maintainer_email='pypi@dataspan.ai',
    url='http://www.dataspan.ai',
    # download_url
    py_modules=['dataspanalgorithms'],
    # scripts
    # ext_modules
    classifiers=[
    ],
    # distclass
    # script_name
    # script_args
    # options
    license='MIT License (MIT)',
    keywords=list(set([
        'dummy',
        'dataspanalgorithms',
        'dataspanalgorithms',
    ])),
    platforms=[
        'any'
    ],
    # data_files
    # package_dir
    # obsoletes
    # provides
    # requires
    # command_packages
    # command_options
    package_data={
        '': [
            'LICENSE',
            'README.md',
        ],
    },
    # include_package_data
    # libraries
    # headers
    # ext_package
    # include_dirs
    # password
    # fullname
    # long_description_content_type
    # python_requires
    # zip_safe,
    # install_requires
)

try:
    from setuptools import setup

    attrs.update(dict(
        include_package_data=True,
        # libraries
        # headers
        # ext_package
        # include_dirs
        # password
        # fullname
        long_description_content_type='text/markdown',
        # python_requires
        zip_safe=True,
    ))
except ImportError:
    from distutils.core import setup

# set-up script for pip distribution
setup(**attrs)

# warn about the package
warnings.warn('This is a dummy package for `dataspanalgorithms`. ')
