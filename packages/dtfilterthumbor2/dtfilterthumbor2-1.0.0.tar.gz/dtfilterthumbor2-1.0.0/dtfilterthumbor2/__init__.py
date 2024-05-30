#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
__version__ = '0.0.2'

logging.info ("setup log")
logger = logging.getLogger('watermarkdt2')
logger.setLevel(logging.DEBUG)
log_file = '/var/log/thumbor.log'
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.info ("success setup logging")
__all__ = ['watermarkdt2']


try:
    from dtfilterthumbor.dtwatermark import Filter  # NOQA
except ImportError:
    logging.exception('Could not import thumbor_text_filter. Probably due to setup.py installing it.')
