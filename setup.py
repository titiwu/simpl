# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 21:20:02 2017

@author: mb
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'simpl - A Simple Music Player',
    'author': 'Matthias Busl',
    'url': 'https://github.com/titiwu/simpl',
    'download_url': 'https://github.com/titiwu/simpl',
    'author_email': 'matthias.busl@gmail.com',
    'version': '0.1',
    'install_requires': ['nose',  'mpd'],
    'packages': ['simpl'],
    'scripts': [],
    'name': 'simpl'
}

setup(**config)
