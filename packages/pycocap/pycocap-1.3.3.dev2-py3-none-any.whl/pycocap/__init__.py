# -*- coding: utf-8 -*-
"""
Purpose
=======

pyCOCAP is the Python interface to the common COCAP database.

Functions
=========

.. currentmodule:: pycocap.pycocap

.. autosummary::
    :toctree: generated

    cases
    deaths
    nfc
    npi
    npis
    reports
    reports_nuts1
    reports_nuts3
    timeseries
"""

from pycocap import pycocap
from pycocap.pycocap import (
    cases,
    deaths,
    nfc,
    npi,
    npis,
    reports,
    reports_nuts1,
    reports_nuts3,
    timeseries,
)

try:
    from pycocap._version import __version__
except ModuleNotFoundError:
    # package is not installed
    __version__ = '0.0.0.dev0'

__all__ = ['__version__']
__all__ += [
    'cases',
    'deaths',
    'nfc',
    'npi',
    'npis',
    'reports',
    'reports_nuts1',
    'reports_nuts3',
    'timeseries',
]
