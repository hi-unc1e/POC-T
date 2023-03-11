#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = unc1e
import json
import traceback

import requests
from lib.core.data import logger
from lib.core.datatype import AttribDict
from lib.utils.versioncheck import PYVERSION


def urljoin_ex(url, path):
    try:
        if PYVERSION >= "3.0":
            from urllib.parse import urljoin
        else:
            from urlparse import urljoin

        return urljoin(url, path)

    except:
        return url.rstrip('/') + "/" + path.lstrip("/")


def get_schemed_url(url):
    schemed_url = url if '://' in url else 'http://' + url
    return schemed_url


def request(method, url, **kwargs):
    resp = None
    try:
        resp = requests.request(method, url, **kwargs)

    # except requests.exceptions.Timeout or requests.exceptions.ConnectionError:
    #     # ReadTimeout/ConnectTimeout
    #     pass

    except:
        pass
        logger.warning(traceback.format_exc())

    finally:
        return resp


def _is_valid_json_resp(resp):
    ret = False
    if not resp:
        return ret
    try:
        _text = resp.text
        _json = json.loads(_text)
        ret = True
    # except TypeError or AttributeError:
    except:
        logger.warning(traceback.format_exc())

    finally:
        return ret


def request_and_parse_json(method, url, **kwargs):
    resp = request(method, url, **kwargs)
    if _is_valid_json_resp(resp):
        _dict = json.loads(resp.text)
        return AttribDict(_dict)
    else:
        return None


def GET_and_parse_json(url, **kwargs):
    resp = request("GET", url, **kwargs)
    if _is_valid_json_resp(resp):
        _dict = json.loads(resp.text)
        return AttribDict(_dict)
    else:
        return None

