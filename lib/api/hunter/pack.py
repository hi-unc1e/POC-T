#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = unc1e

import sys
from lib.core.data import paths, logger
from lib.utils.config import ConfigFileParser
from lib.core.common import getSafeExString
import requests
import base64
import json
import base64



def check(token):
    if token:
        # https://hunter.qianxin.com/home/helpCenter?r=5-2
        # curl -X GET -k "https://hunter.qianxin.com/openApi/search?username={username}&api-key={api-key}&search={search}&page=1&page_size=10&is_web=1&start_time="2021-01-01 00:00:00"&end_time="2021-03-01 00:00:00""
        search = 'ip.port=80'
        search = base64.urlsafe_b64encode(search.encode("utf-8"))
        auth_url = "https://hunter.qianxin.com/openApi/search?api-key=%s&search=%s&page=1&page_size=1" % (token, search)

        try:
            response = requests.get(url=auth_url)
            if (response.status_code == 200) and ("success" in response.text):
                return True
        except Exception as e:
            logger.error(e)
            return False
    return False


def HunterSearch(query, limit=10, offset=1):
    try:
        offset = 1 if offset == 0 else offset
        msg = 'Trying to login with credentials in config file: %s.' % paths.CONFIG_PATH
        logger.info(msg)
        token = ConfigFileParser().HunterKey()
        if check(token):
            pass
        else:
            raise  # will go to except block
    except:
        msg = 'Automatic authorization failed.'
        logger.warning(msg)
        msg = 'Please input your hunter.qianxin.com API Key below.'
        logger.info(msg)
        token = raw_input("Hunter api-key: ").strip()
        if not check(token):
            msg = 'Hunter.qianxin.com API authorization failed, Please re-run it and enter a valid key.'
            sys.exit(logger.error(msg))


    url = "https://hunter.qianxin.com/openApi/search?api-key={token}&search={q}&page={page}&page_size={limit}"
    url = url.format(token=token,
                     q=base64.urlsafe_b64encode(query),
                     page=offset,
                     limit=limit
                     )

    #print(request)#
    result = []
    try:
        # https://hunter.qianxin.com/home/helpCenter?r=5-2
        response = requests.get(url, verify=False)
        resp = response.text
        resp = json.loads(resp)
        if resp["code"] == 200:
            total = resp['data']['total']
            for item in resp.get('data').get('arr'):
                ip = item.get('ip')
                port = item.get('port')
                # url
                # url = item.get('url') #
                ret = "%s:%s" % (ip, port)
                result.append(ret)
            if total > limit:
                logger.info("{0} items found! {1} returned....".format(total, limit))
            else:
                logger.info("{0} items found!".format(count))
        elif 400 == resp["code"]:
                logger.warning("Too many reqs, slow down plz!")
        else:
                logger.info("error: "+str(resp))
    except Exception as e:
        sys.exit(logger.error(getSafeExString(e)))
    finally:
        return result
