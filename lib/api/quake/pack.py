#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = unc1e

import sys
from lib.core.data import paths, logger
from lib.utils.config import ConfigFileParser
from lib.core.common import getSafeExString
import getpass
import urllib
import requests
import base64
import json


def check(token):
    if token:
        # X-QuakeToken: d17140ae-xxxx-xxx-xxxx-c0818b2bbxxx
        # https://quake.360.cn/api/v3/search/quake_service
        auth_url = "https://quake.360.cn/api/v3/search/quake_service"

        header = {'X-QuakeToken': token}
        postdata = {"query": "port: 443", "start": 0, "size": 1}

        try:
            response = requests.post(url=auth_url, headers=header, json=postdata)
            if response.status_code == 200:
                return True
        except Exception as e:
            logger.error(e)
            return False
    return False


def QuakeSearch(query, limit=10, offset=0):
    try:
        msg = 'Trying to login with credentials in config file: %s.' % paths.CONFIG_PATH
        logger.info(msg)
        token = ConfigFileParser().QuakeKey()
        if check(token):
            pass
        else:
            raise  # will go to except block
    except:
        msg = 'Automatic authorization failed.'
        logger.warning(msg)
        msg = 'Please input your FoFa Email and API Key below.'
        logger.info(msg)
        token = raw_input("X-QuakeToken: ").strip()
        if not check(token):
            msg = 'X-QuakeToken API authorization failed, Please re-run it and enter a valid key.'
            sys.exit(logger.error(msg))


    header = {'X-QuakeToken': token}
    post_query = {"query": "port: 443", "start": offset, "size": limit}
    url = "https://quake.360.cn/api/v3/search/quake_service"
    #print(request)#
    result = []
    try:
        response = requests.post(url, headers=header, json=post_query)
        resp = response.content
        resp = json.loads(resp)
        if resp["code"] == 0:
            count = resp['meta']['pagination']['count']
            total = resp['meta']['pagination']['total']
            for item in resp.get('data'):
                ip = item.get('ip')
                port = item.get('port')
                ret = "%s:%s" % (ip, port)
                result.append(ret)
            if count > limit:
                logger.info("{0} items found! {1} returned....".format(total, limit))
            else:
                logger.info("{0} items found!".format(count))
    except Exception as e:
        sys.exit(logger.error(getSafeExString(e)))
    finally:
        return result
