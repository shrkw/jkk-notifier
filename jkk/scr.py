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
    call(os.environ.get('MAIL_RECIPIENT'), u'アイルレンジャク')

def call(recipient, q_word):
    s = Searcher()
    soup = s.search(q_kana=q_word)
    err = soup.find('li', class_='error')
    if err and u'空室はございません' in err.text:
        send_search_result(recipient, u'JKK検索結果: 見つかりませんでした: %s' % q_word, { "title": u'JKK検索結果: 見つかりませんでした: %s' % q_word, "lead": u'10分おきに検索します', "query": q_word})
    elif err:
        send_search_result(recipient, u'JKK検索結果: エラーがおきました: %s' % q_word, { "title": u'JKK検索結果: エラーがおきました: %s' % q_word, "lead": err.text, "query": q_word})
    else:
        send_search_result(recipient, u'JKK検索結果: 見つかりました: %s' % q_word, { "title": u'JKK検索結果: 見つかりました: %s' % q_word, "lead": u'すぐにチェックして申し込みましょう', "query": q_word})
