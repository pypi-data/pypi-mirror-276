#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
__version__ = '0.0.2'

try:
    logging.info ("start import watermarkdt2.watermarkdt2")
    from watermarkdt2.watermarkdt2 import Filter
    logging.info ("success import watermarkdt2.watermarkdt2")
except ImportError:
    logging.exception('Could not import thumbor_text_filter. Probably due to setup.py installing it.')