#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = unc1e
import json
import traceback

import requests
from lib.core.data import th, conf, logger, paths


def request(method, url, **kwargs) -> requests.Response or None:
    resp = None
    try:
        resp = requests.request(method, url, **kwargs)

    except:
        logger.warning(traceback.format_exc())

    finally:
        return resp


def _is_valid_json_resp(resp):
    ret = False
    try:
        _text = resp.text
        _json = json.loads(_text)
        ret = True
    # except TypeError:
    #     ret = False
    #
    # except AttributeError:
    #     ret = False
    except:
        logger.warning(traceback.format_exc())

    finally:
        return ret


def json_load_ex(method, url, **kwargs) -> dict:
    resp = request(method, url, **kwargs)
    if _is_valid_json_resp(resp):
        return json.loads(resp.text)
    else:
        return None


