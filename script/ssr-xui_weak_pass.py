#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   xui-ssr-weak-pass.py.py    
@DateTime :  2023/3/11 18:01
@Usage:


'''

import requests

from utils.versioncheck import PYVERSION


def get_schemed_url(url):
    schemed_url = url if '://' in url else 'http://' + url
    return schemed_url


def urljoin_ex(url, path):
    try:
        if PYVERSION >= "3.0":
            from urllib.parse import urljoin
        else:
            from urlparse import urljoin

        return urljoin(url, path)

    except:
        return url.rstrip('/') + "/" + path.lstrip("/")

password = ""

def _get_post_data(pwd):
    post_data = {
        "username": "admin",
        "password": "admin"
    }


def poc(url):
    url = get_schemed_url(url)
    login_url = urljoin_ex(url, "login")


    r = requests.post(login_url, )
    return True