#!/bin/env python
# encoding: UTF-8

import os
import pymongo

import logging
from .logger import handler
logger = logging.getLogger(__name__)
logger.addHandler(handler)

url = os.environ.get('MONGODB_URI')
client = pymongo.MongoClient(url)

def get_collection(name):
    db = client[url.split('/')[-1]]
    co = db[name]
    return co
