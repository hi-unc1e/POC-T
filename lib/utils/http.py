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
    url = get_http_url(url)
    try:
        if PYVERSION >= "3.0":
            from urllib.parse import urljoin
        else:
            from urlparse import urljoin

        return urljoin(url, path)

    except:
        return url.rstrip('/') + "/" + path.lstrip("/")


def get_http_url(url_or_hostPort):
    """
    :input
        1.2.3.4:80
        http://1.2.3.4:80/
        1.2.3.4


    :output
    """
    xstr = str(url_or_hostPort)

    matches = {
        "443": "https",
        "80": "http"
    }
    if "//" not in xstr:
        if xstr.__contains__("443"):
            xstr = "https://" + xstr

        elif xstr.__contains__("80"):
            xstr = "http://" + xstr

        else:
            # 默认https
            xstr = "https://" + xstr

    xstr = xstr.rstrip('/')
    return xstr


def request_ex(method, url, **kwargs):
    resp = None
    try:
        kwargs["verify"] = False
        kwargs["timeout"] = 15
        resp = requests.request(method, url, **kwargs)

    except requests.exceptions.Timeout:
        logger.warning("Timeout error")
        logger.warning(traceback.format_exc())

    except requests.exceptions.ConnectionError:
    #     # ReadTimeout/ConnectTimeout
        logger.warning("ConnectionError")
        logger.warning(traceback.format_exc())

    except:
        logger.warning("ConnectionError")
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
    resp = request_ex(method, url, **kwargs)
    if _is_valid_json_resp(resp):
        _dict = json.loads(resp.text)
        return AttribDict(_dict)
    else:
        return None


def GET_and_parse_json(url, **kwargs):
    resp = request_ex("GET", url, **kwargs)
    if _is_valid_json_resp(resp):
        _dict = json.loads(resp.text)
        return AttribDict(_dict)
    else:
        return None

