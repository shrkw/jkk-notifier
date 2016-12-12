#!/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import
import os
import pymongo

from .mailer import send_search_result
from .mongo import get_collection
from .searcher import Searcher

import logging
from .logger import handler
logger = logging.getLogger(__name__)
logger.addHandler(handler)

def run(force_send=False):
    co = get_collection('conditions')
    for row in co.find():
        call(force_send, str(row['_id']), row['recipient'], row['q_word'])

def call(force_send, id_, recipient, q_word):
    s = Searcher()
    soup = s.search(q_kana=q_word)
    err = soup.find('li', class_='error')
    subject, lead, found = collect(err, q_word)

    co = get_collection('search_histories')
    rows = list(co.find({"condition_id": id_}).sort('_id', pymongo.DESCENDING).limit(1))
    co.insert_one({"condition_id": id_, "found": found, "subject": subject, "q_word": q_word})
    # treat the status is changed when first search
    status_changed = len(rows) == 0 or rows[0]['found'] != found
    if force_send or status_changed:
        send_search_result(recipient, subject, { "title": subject, "lead": lead, "query": q_word})

def collect(err, q_word):
    if err and u'空室' in err.text:
        subject = u'JKK検索結果: 見つかりませんでした: %s' % q_word
        lead = u'10分おきに検索します'
        found = False
    elif err:
        subject = u'JKK検索結果: エラーがおきました: %s' % q_word
        lead = err.text
        found = False
    else:
        subject = u'JKK検索結果: 見つかりました: %s' % q_word
        lead = u'すぐにチェックして申し込みましょう'
        found = True
    return (subject, lead, found)
