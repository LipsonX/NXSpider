#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/12/15.
# email to LipsonChan@yahoo.com
#

import os

if os.name == "nt":
    def symlink_ms(source, link_name):
        import ctypes
        csl = ctypes.windll.kernel32.CreateSymbolicLinkW
        csl.argtypes = (ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32)
        csl.restype = ctypes.c_ubyte
        flags = 1 if os.path.isdir(source) else 0
        try:
            if csl(link_name, source.replace('/', '\\'), flags) == 0:
                raise ctypes.WinError()
        except Exception as e:
            pass


    os.symlink = symlink_ms


def symlink(source, link_name):
    try:
        os.symlink(source, link_name)
    except Exception as e:
        pass


# a = os.getcwd()
# src = os.path.join(a, "install.bat")
# dst = os.path.join(a, "test.link")
#
# os.symlink(os.path.join(a, "install.bat"), os.path.join(a, "test.link"))
