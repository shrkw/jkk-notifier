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
    s = Searcher()
    qq = u'アイルレンジャク'
    soup = s.search(q_kana=qq)
    err = soup.find('li', class_='error')
    if err and u'空室はございません' in err.text:
        send_search_result(os.environ.get('MAIL_RECIPIENT'), u'JKK検索結果: 見つかりませんでした: %s' % qq, { "title": u'JKK検索結果: 見つかりませんでした: %s' % qq, "lead": u'10分おきに検索します', "query": qq})
    elif err:
        send_search_result(os.environ.get('MAIL_RECIPIENT'), u'JKK検索結果: エラーがおきました: %s' % qq, { "title": u'JKK検索結果: エラーがおきました: %s' % qq, "lead": err.text, "query": qq})
    else:
        send_search_result(os.environ.get('MAIL_RECIPIENT'), u'JKK検索結果: 見つかりました: %s' % qq, { "title": u'JKK検索結果: 見つかりました: %s' % qq, "lead": u'すぐにチェックして申し込みましょう', "query": qq})
