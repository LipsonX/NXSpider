#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/4/16.
# email to LipsonChan@yahoo.com
#

import json
import os

from NXSpider.common import encrypt
from NXSpider.common import tools, log

csrf_dict = {'csrf_token': 'csrf'}


def encrypted_request(obj):
    data = {
        'params': create_params_by_dict(obj),
        'encSecKey': encSecKey
    }
    return data


def create_params_by_dict(obj):
    try:
        return create_params_text(json.dumps(obj))
    except Exception as e:
        log.print_err('create params error: %s' % e)
        return None


def create_params_text(text):
    nonce = '0CoJUm6Qyw8W8jud'
    nonce2 = 16 * 'F'
    encText0 = encrypt.aes(text, nonce).decode("utf-8")
    encText = encrypt.aes(encText0, nonce2)
    return encText


def decrpyt_params(text):
    nonce = '0CoJUm6Qyw8W8jud'
    nonce2 = 16 * 'F'
    decText0 = encrypt.aes_decode(text, nonce2)
    decText = encrypt.aes_decode(decText0, nonce)
    return decText


def rsa_encrypt(text, pubKey, modulus):
    text = text[::-1]
    rs = int(tools.hex(text), 16) ** int(pubKey, 16) % int(modulus, 16)
    return format(rs, 'x').zfill(256)


def create_secretKey(size):
    return (
               ''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size)))
           )[0:16]


modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
pubKey = '010001'
secKey = 16 * 'F'
encSecKey = rsa_encrypt(secKey, pubKey, modulus)
