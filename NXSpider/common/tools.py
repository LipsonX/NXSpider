#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MIT License

Copyright (c) 2017 Cheng YuMeng

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import codecs
import contextlib
import hashlib
import locale

from NXSpider.common import PYTHON3

RETURN_JSON = "return json data"
RETURE_HTML = "return html data"

lang, sys_encoding = locale.getdefaultlocale()

@contextlib.contextmanager
def ignored(*exceptions):
    try:
        yield
    except exceptions:
        pass


def encode(s):
    if PYTHON3 is True:
        return codecs.encode(s, "utf-8").decode("utf-8")
    else:
        return s.encode("utf-8")


def encode_sys(s):
    s.encode(sys_encoding)


def hex(s):
    if PYTHON3 is True:
        return codecs.encode(bytes(s, encoding="utf8"), 'hex')
    else:
        return s.encode("hex")


def md5(s):
    m = hashlib.md5()
    m.update(s.encode("utf-8"))
    return m.hexdigest()


def is_unicode(obj):
    if PYTHON3:
        return isinstance(obj, str)
    else:
        from __builtin__ import unicode
        return isinstance(obj, unicode)


def input_format(string):
    """
    :type string: str
    :param string:
    :return:
    """
    if PYTHON3:
        return string
    else:
        return string.encode()

