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
import time



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

def req(url):
    global total
    try:
        response = requests.get(url, verify=False)
        resp = response.text
        resp = json.loads(resp)
        if resp["code"] == 200:
            count = len(resp['data']['arr'])
            total = len(resp['data']['total'])
            logger.info("{0} items found!".format(count))

            for item in resp.get('data').get('arr'):
                ip = item.get('ip')
                port = item.get('port')
                # url
                # url = item.get('url') #
                ret = "%s:%s" % (ip, port)
                return resp["code"],ret
        else:
            return resp["code"],None
    except Exception as e:
        logger.warning(e)
        return False, None


def HunterSearch(query, limit=10, offset=1):
    global total
    total = limit
    offset = 1 if offset == 0 else offset
    try:
        MAX_LENGTH_PER_PAGE = 100
        MAX_RETRY_TIMES = 2
        # 201
        loop_time = (limit//MAX_LENGTH_PER_PAGE)  # 2
        loop_dict = {}
        for i in range(loop_time): # 0, 1
            page = i+1
            # 1: 100
            # 2: 100
            loop_dict[offset+page+1] = MAX_LENGTH_PER_PAGE

        # 3: 011
        loop_dict[loop_time+1] = int(limit-MAX_LENGTH_PER_PAGE*loop_time)

        # offset>0

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

    result = []
    try:
        for page,size in loop_dict.items():
            url = "https://hunter.qianxin.com/openApi/search?api-key={token}&search={q}&page={page}&page_size={limit}"
            url = url.format(token=token,
                             q=base64.urlsafe_b64encode(query),
                             page=page,
                             limit=size
                             )

            # https://hunter.qianxin.com/home/helpCenter?r=5-2
            code,ret = req(url)
            if ret != None:
                result.append(ret)
            if total > limit and code == 200:
                logger.info("{0} items found! {1} returned....".format(total, limit))
            elif 429 == code:
                while (MAX_RETRY_TIMES > 0):
                    logger.warning("[%s]Too many reqs, slow down plz!" % MAX_RETRY_TIMES)
                    time.sleep(10)
                    MAX_RETRY_TIMES -= 1
                    code,ret = req(url)
                    if ret != None and code == 200:
                        result.append(ret)
                        # ok
                        break
                    else:
                        # or
                        continue
            else:
                logger.info("error: "+str(code))
    except Exception as e:
        sys.exit(logger.error(getSafeExString(e)))
    finally:
        return result
