#!/bin/env python
# encoding: UTF-8

from __future__ import division, print_function, absolute_import
import argparse

import sys
import os
sys.path.append(os.getcwd())

from jkk import scr

import logging
from jkk.logger import handler
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


if __name__ == "__main__":
    logger.info("start")
    import datetime
    import pytz
    now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
    if now.hour in range(9, 18):
        try:
            scr.run()
        except Exception as e:
            logger.error('Error: ', exc_info=True)
    else:
        logger.info("was not executed, %s" % now)
    logger.info("end")
