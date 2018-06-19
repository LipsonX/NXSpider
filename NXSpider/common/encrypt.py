#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/4/19.
# email to LipsonChan@yahoo.com
#

import base64

from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)
from cryptography.hazmat.backends import default_backend


def aes(text, sec_key):
    backend = default_backend()
    pad = 16 - len(text) % 16
    text_t = text + pad * chr(pad)
    cipher = Cipher(
        algorithms.AES(sec_key.encode('utf-8')),
        modes.CBC(b'0102030405060708'),
        backend=backend
    )
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(text_t.encode('utf-8')) + encryptor.finalize()
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext

def aes_ecb_decode(text, sec_key):
    backend = default_backend()
    ciphertext = base64.b64decode(text)
    cipher = Cipher(
        algorithms.AES(sec_key.encode('utf-8')),
        modes.ECB(),
        backend=backend
    )
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext

def aes_ecb(text, sec_key):
    backend = default_backend()
    text = text.encode('utf-8')
    pad = 16 - len(text) % 16
    text_t = text + (b'\0' * pad)
    cipher = Cipher(
        algorithms.AES(sec_key.encode('utf-8')),
        modes.ECB(),
        backend=backend
    )
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(text_t) + encryptor.finalize()
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext