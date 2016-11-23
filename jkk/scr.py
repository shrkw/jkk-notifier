#!/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import
from bs4 import BeautifulSoup
import requests
import os

from .mailer import send

import logging
from .logger import handler
logger = logging.getLogger(__name__)
logger.addHandler(handler)

def run():
    s = requests.Session()
    token = get_token(s)
    soup = search(s, token)
    rows = soup.find_all("table", class_="cell666666")[1].select('tr')
    rows = [row.find('td').text.strip() for row in rows]
    q = u'アイル連雀'
    if q in rows:
        subject = u'JKK検索結果: 見つかりました: %s' % q
    else:
        subject = u'JKK検索結果: 見つかりませんでした: %s' % q
    body = '\n'.join(rows)
    send(os.environ.get('MAIL_RECIPIENT'), subject, body)

def get_token(s):
    payload = {'redirect': 'true', 'link_id': '01' }
    r = s.post('https://jhomes.to-kousya.or.jp/search/jkknet/service/akiyaJyoukenStartInit', data=payload)
    r.encoding = 'CP932'
    soup = BeautifulSoup(r.text, "html.parser")
    token = soup.find(attrs={"name":"token"})['value']
    return token

def search(s, token):
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        'Origin': 'https://jhomes.to-kousya.or.jp',
        'Referer': 'https://jhomes.to-kousya.or.jp/search/jkknet/service/akiyaJyokenDirect' }

    query = {
        'akiyaInitRM.akiyaRefM.checks': '34',
        'akiyaInitRM.akiyaRefM.yachinFrom': '0',
        'akiyaInitRM.akiyaRefM.yachinTo': '999999999',
        'akiyaInitRM.akiyaRefM.mensekiFrom': '0',
        'akiyaInitRM.akiyaRefM.mensekiTo': '9999.99',
        'akiyaInitRM.akiyaRefM.yusenBoshu': '',
        'akiyaInitRM.akiyaRefM.jyutakuKanaName': '',
        'akiyaInitRM.akiyaRefM.ensenCd': '',
        'akiyaInitRM.akiyaRefM.mskKbn': '',
        'token': token,
        'abcde': 'EF8F0627B5A8184A6BA3E8705A00F068',
        'jklm': 'E17511BF89D3A101AFEF10EBF1587561',
        'sen_flg': '1',
        'akiyaInitRM.akiyaRefM.allCheck': '',
        'akiyaInitRM.akiyaRefM.madoris': '',
        'akiyaInitRM.akiyaRefM.tanshinFlg': '',
        'akiyaInitRM.akiyaRefM.teishiKaiFlg': '',
        'akiyaInitRM.akiyaRefM.yuguFlg': ''
    }
    r = s.post('https://jhomes.to-kousya.or.jp/search/jkknet/service/akiyaJyoukenRef', headers=headers, data=query)
    r.encoding = 'CP932'
    soup = BeautifulSoup(r.text, "html.parser")
    return soup
