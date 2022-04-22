#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = unc1e

import sys
import traceback

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
    try:
        response = requests.get(url, verify=False)
        return response

    except Exception as e:
        logger.warning(e)
        return None

def parse_arr(resp):
    res = []
    for item in resp.get('data').get('arr'):
        ip = item.get('ip')
        port = item.get('port')
        # url
        url = item.get('url') #
        ret = "%s:%s" % (ip, port) if url == '' else url
        if ret != '':
            res.append(ret)
        return res

def HunterSearch(query, limit=10, offset=1):
    page = offset
    page_size = limit
    MAX_LENGTH_PER_PAGE = 100
    loop_dict = {}

    if page_size <= MAX_LENGTH_PER_PAGE:
        # < 100
        page = 1
        loop_dict[page] = page_size
        pass
    else:
        # > 100

        # eg: page_size->201
        loop_time = (page_size//MAX_LENGTH_PER_PAGE)+1  # 2
        for i in range(1, loop_time): # 0, 1
            page = i
            # 1: 100
            # 2: 100
            loop_dict[i] = MAX_LENGTH_PER_PAGE

        # 3: 011
        loop_dict[loop_time] = int(page_size-(MAX_LENGTH_PER_PAGE*(loop_time-1)))

    try:
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
        MAX_RETRY_TIMES = 2
        for page,size in loop_dict.items():
            url = "https://hunter.qianxin.com/openApi/search?api-key={token}&search={q}&page={page}&page_size={size}&is_web=1"
            url = url.format(token=token,
                             q=base64.urlsafe_b64encode(query),
                             page=page,
                             size=size
                             )

            # https://hunter.qianxin.com/home/helpCenter?r=5-2
            r = req(url)
            if r == None:
                exit("request error:(%s)" % url)
            resp = r.text
            resp = json.loads(resp)
            code = resp["code"]
            if code == 200:
                count = len(resp['data']['arr'])
                total = resp['data']['total']
                logger.info("{0} items found!".format(count))

                if total > limit and code == 200 and page == 1:
                    logger.info("{0} items found! {1} returned....".format(total, limit))

                ret = parse_arr(resp)
                result.extend(ret)
                continue
            #
            elif 429 == code:
                while (MAX_RETRY_TIMES > 0):
                    logger.warning("[%s]Too many reqs, slow down plz!(%s)" % (MAX_RETRY_TIMES, r.text))
                    time.sleep(8)
                    MAX_RETRY_TIMES -= 1
                    r = req(url)
                    resp = r.text
                    resp = json.loads(resp)
                    code = resp["code"]
                    if code == 200:
                        count = len(resp['data']['arr'])
                        logger.info("{0} items found!".format(count))
                        ret = parse_arr(resp)
                        result.extend(ret)
                        # ok
                        break
                    else:
                        # or
                        continue
            else:
                logger.info("error: "+str(resp))
            time.sleep(5)
            continue
    except Exception as e:
        traceback.print_exc(e)
        sys.exit(logger.error(getSafeExString(e)))
    finally:
        return result
