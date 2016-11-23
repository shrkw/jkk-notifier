#!/bin/env python
# encoding: UTF-8

import urllib.request
import urllib.parse
from collections import namedtuple

from bs4 import BeautifulSoup
from TwitterAPI import TwitterAPI

from .config import *  # noqa

import logging
from .logger import handler
logger = logging.getLogger(__name__)
logger.addHandler(handler)

Schedule = namedtuple("Schedule", ["date", "time", "url"])


def check(q):
    b = "http://tv.yahoo.co.jp/search/?q=%s&g=&Submit.x=0&Submit.y=0"
    url = b % urllib.parse.quote_plus(q)
    res = BeautifulSoup(urllib.request.urlopen(url))
    cnt = res.find_all("span", attrs={"class": "yjL"})[1]
    if int(cnt.text) is not 0:
        left = res.find("div", attrs={"class": "leftarea"})
        child = left.findChild('p')
        return Schedule(child.text, child.nextSibling.nextSibling.text, url)
    else:
        return None


def tweet(s):
    api = TwitterAPI(TWI_CONSUMER_KEY,
                     TWI_CONSUMER_SECRET,
                     TWI_ACCESS_TOKEN_KEY,
                     TWI_ACCESS_TOKEN_SECRET)
    r = api.request('statuses/update', {'status': s})
    logger.info("twitter response code: %s" % (r.status_code))
    logger.debug("twitter response text: %s" % (r.text))
    if r.status_code != 200:
        logger.warn("headers: %s" % (r.headers))


def run(q):
    schedule = check(q)
    if schedule is not None:
        logger.info("found: %s" % q)
        tweet("@%s %sの放送が予定されています。 %s %s %s" %
              ("shrkwh", q, schedule.date, schedule.time, schedule.url))
    else:
        logger.info("not found: %s" % q)
