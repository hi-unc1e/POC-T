#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   chatgpt_public.py    
@Contact :   lihanwei@zhiqiansec.com
@DateTime :  2023/5/13 11:39 
'''
from lib.utils.http import request_ex, get_http_url, urljoin_ex

import requests
import json
import time


"""
fid="qObSo5JrR9FIkIqprX7XKg=="
"""

def is_chat_api_valid(url):
    prompt="中国的首都在哪里?"
    kw = "北京"
    url = urljoin_ex(url, "/chat-process")
    headers = {"Content-Type": "application/json"}
    payload = {
        "prompt": prompt,
        "systemMessage": "test",
        "temperature": 0.5,
        "top_p": 0.5
    }
    
    response = request_ex('post', url, headers=headers, data=json.dumps(payload),stream=True)
    if not response or response.status_code != 200:
        print("error")
        return None
    #print(response.status_code)
    #print(response.text)
    text_value = []
    for chunk in response.iter_lines():
        #print(str(chunk))
        data = json.loads(chunk)
        text_value = data.get("text")
        return text_value != None
    #     if text_value != None:
    #         print(text_value)


def poc(url):
    return is_chat_api_valid(url)


if __name__ == "__main__":
    a = poc("http://82.157.52.147:3002/")
    print(a)
