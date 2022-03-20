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
        auth_url = "hhttps://quake.360.cn/api/v3/search/quake_service"

        header = {'X-QuakeToken': token}
        postdata = {"query": "port: 443", "start": 0, "size": 1}

        try:
            response = requests.post(url=auth_url, header=header, json=postdata)
            if response.code == 200:
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

    query = base64.b64encode(query)

    request = "https://fofa.info/api/v1/search/all?email={0}&key={1}&qbase64={2}&size={3}&page={4}".format(email, key, query, limit, offset)
    #print(request)#
    result = []
    try:
        response = urllib.urlopen(request)
        resp = response.readlines()[0]
        resp = json.loads(resp)
        if resp["error"] is False: # /opt/POC-T/lib/api/fofa/pack.py:59turn none to false, fix no result to return!
            for item in resp.get('results'):
                #print(item)
                result.append(item[0])
            if resp.get('size') >= 100 and resp.get('size') > limit  : # real< limit
                logger.info("{0} items found! {1} returned....".format(resp.get('size'), limit))
            else:# real < 100 or limit > real
                logger.info("{0} items found!".format(resp.get('size')))
    except Exception as e:
        sys.exit(logger.error(getSafeExString(e)))
    finally:
        return result
