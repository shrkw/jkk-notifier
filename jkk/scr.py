#!/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import
import os

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
        call(row['recipient'], row['q_word'])

def call(recipient, q_word):
    s = Searcher()
    soup = s.search(q_kana=q_word)
    err = soup.find('li', class_='error')
    if err and u'空室' in err.text:
        subject = u'JKK検索結果: 見つかりませんでした: %s' % q_word
        lead = u'10分おきに検索します'
    elif err:
        subject = u'JKK検索結果: エラーがおきました: %s' % q_word
        lead = err.text
    else:
        subject = u'JKK検索結果: 見つかりました: %s' % q_word
        lead = u'すぐにチェックして申し込みましょう'
    send_search_result(recipient, subject, { "title": subject, "lead": lead, "query": q_word})
