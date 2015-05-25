#!/usr/bin/env python

from setuptools import setup

setup(
    name = 'bip32utils',
    version = '0.2',
    author = 'Johnathan Corgan, Corgan Labs',
    author_email = 'johnathan@corganlabs.com',
    url = 'http://github.com/jmcorgan/bip32utils',
    description = 'Utilities for generating and using Bitcoin Hierarchical Deterministic wallets (BIP0032).',
    license = 'MIT',
    requires = ['ecdsa'],
    packages = ['bip32utils'],
    scripts = ['bin/bip32gen']
)
