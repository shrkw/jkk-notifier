#!/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import
from bs4 import BeautifulSoup
import requests

import logging
from .logger import handler
logger = logging.getLogger(__name__)
logger.addHandler(handler)

class Searcher:
    def __init__(self):
        self.session = requests.Session()
        self.token = self.get_token()

    def search(self, q_city_code='', q_kana=''):
        headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
            'Origin': 'https://jhomes.to-kousya.or.jp',
            'Referer': 'https://jhomes.to-kousya.or.jp/search/jkknet/service/akiyaJyokenDirect' }
        query = {
            'akiyaInitRM.akiyaRefM.checks': q_city_code,
            'akiyaInitRM.akiyaRefM.yachinFrom': '0',
            'akiyaInitRM.akiyaRefM.yachinTo': '999999999',
            'akiyaInitRM.akiyaRefM.mensekiFrom': '0',
            'akiyaInitRM.akiyaRefM.mensekiTo': '9999.99',
            'akiyaInitRM.akiyaRefM.yusenBoshu': '',
            'akiyaInitRM.akiyaRefM.jyutakuKanaName': q_kana.encode('shift-jis'),
            'akiyaInitRM.akiyaRefM.ensenCd': '',
            'akiyaInitRM.akiyaRefM.mskKbn': '',
            'token': self.token,
            'abcde': 'EF8F0627B5A8184A6BA3E8705A00F068',
            'jklm': 'E17511BF89D3A101AFEF10EBF1587561',
            'sen_flg': '1',
            'akiyaInitRM.akiyaRefM.allCheck': '',
            'akiyaInitRM.akiyaRefM.madoris': '',
            'akiyaInitRM.akiyaRefM.tanshinFlg': '',
            'akiyaInitRM.akiyaRefM.teishiKaiFlg': '',
            'akiyaInitRM.akiyaRefM.yuguFlg': ''
        }
        r = self.session.post('https://jhomes.to-kousya.or.jp/search/jkknet/service/akiyaJyoukenRef', headers=headers, data=query)
        r.encoding = 'CP932'
        soup = BeautifulSoup(r.text, "html.parser")
        return soup

    def get_token(self):
        payload = {'redirect': 'true', 'link_id': '01' }
        r = self.session.post('https://jhomes.to-kousya.or.jp/search/jkknet/service/akiyaJyoukenStartInit', data=payload)
        r.encoding = 'CP932'
        soup = BeautifulSoup(r.text, "html.parser")
        token = soup.find(attrs={"name":"token"})['value']
        return token
