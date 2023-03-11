#coding:utf-8
'''
python POC-T.py -s proxy_pool_all -aF "title=\"Welcome to Proxy Pool System\""
'''
from urlparse import urljoin
import requests
import json


TIMEOUT = 3
URL = "https://httpbin.org/ip"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    }


def test_all_ip(ips):
    r = requests.get(URL, timeout=TIMEOUT)
    rj = json.loads(r.text)
    old_ip = rj.get("origin")
    good_proxy = []
    for ip in ips:
        PROXY = {
            "http": "http://%s" % ip,
            "https": "https://%s" % ip
        }
        r = requests.get(URL, timeout=TIMEOUT, proxies=PROXY)
        rj = json.loads(r.text)
        new_ip = rj.get("origin")
        if new_ip != old_ip:
            good_proxy.append(ip)
        else:
            pass
    return set(new_ip)


def poc(url):
    all_url = urljoin(url, "all")

    # 可访问
    #print url
    try:
        r = requests.get(url=all_url, headers=headers, timeout=TIMEOUT, verify=False)
        ips = r.text.split('\n')
        good_ips = test_all_ip(ips)
        return good_ips
    except:
        return False
        
#print(poc("proxy.lfk.qianxin-inc.cn:3128"))


