#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = bit4

import sys

import requests

from lib.core.convert import stdoutencode
from lib.core.data import paths, logger
from lib.utils.config import ConfigFileParser
from lib.utils.http import GET_and_parse_json
from lib.core.common import getSafeExString
import getpass
import base64
import json

from lib.utils.versioncheck import PY2


def check(email, key):
    if email and key:
        auth_url = "https://fofa.info/api/v1/info/my?email={0}&key={1}".format(email, key)
        try:
            r_dict = GET_and_parse_json(auth_url, verify=False)
            if r_dict.error:
                return False
            else:
                return True
        except Exception as e:
            logger.error(e)
            return False
    return False


def get_fofa_query(query):
    if PY2:
        query_b = query
    else:
        query_b = stdoutencode(query)
    query = base64.b64encode(query_b)
    if isinstance(query, bytes):
        query = query.decode()
    return query


def get_fofa_info_or_exit():
    email = ""
    key = ""
    try:
        msg = 'Trying to login with credentials in config file: %s.' % paths.CONFIG_PATH
        logger.info(msg)
        email = ConfigFileParser().FofaEmail()
        key = ConfigFileParser().FofaKey()
        if check(email, key):
            pass
        else:
            raise  # will go to except block
    except:
        msg = 'Automatic authorization failed.'
        logger.warning(msg)
        msg = 'Please input your FoFa Email and API Key below.'
        logger.info(msg)
        email = input("Fofa Email: ").strip()
        key = getpass.getpass(prompt='Fofa API Key: ').strip()
        if not check(email, key):
            msg = 'Fofa API authorization failed, Please re-run it and enter a valid key.'
            logger.error(msg)
            # sys.exit(logger.error(msg))
    finally:
        return email, key


def detect_http_or_https(ip, port):
    host = "%s:%s" % (ip, port)
    urls = ("https://%s" % host, "http://%s" % host)

    for url in urls:
        try:
            response = requests.get(url, timeout=5, verify=False)
            response.raise_for_status()
            return url
        except requests.RequestException:
            continue

    return None

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


def FofaSearch(query, limit=100, offset=0):  # DONE 付费获取结果的功能实现
    page = offset + 1
    email, key = get_fofa_info_or_exit()

    b64_query = get_fofa_query(query)
    url = "https://fofa.info/api/v1/search/all?email={0}&key={1}&qbase64={2}&size={3}&page={4}".format(email, key,
                                                                                                       b64_query, limit,
                                                                                                       page)
    resp = GET_and_parse_json(url, verify=False)

    # check err
    if resp.error != False:
        msg = "error! query: %s, resp: %s"  % (query, resp)
        logger.error(msg)
        exit()

    # via page
    result = []

    for item in resp.results:
        # print(item)
        url_or_hostPort = item[0]
        url = get_http_url(url_or_hostPort)
        result.append(url)
    if resp.size >= 100 and resp.size > limit:  # real< limit
        logger.info("{0} items found! {1} returned....".format(resp.get('size'), limit))
    else:  # real < 100 or limit > real
        logger.info("{0} items found!".format(resp.get('size')))

    return result