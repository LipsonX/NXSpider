#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/6/20.
# email to LipsonChan@yahoo.com
#
import sys

from cement.core.controller import CementBaseController

from NXSpider.common import log, PYTHON2
from NXSpider.common.constant import all_download_type


def py2_decoding(string):
    if PYTHON2:
        return string.decode(sys.getfilesystemencoding())
    return string

def py2_encoding(string):
    if PYTHON2:
        return string.encode('utf8')


class NXSpiderBaseController(CementBaseController):
    def parse_download(self):
        """
        lost of spider function will parse -dw param, this will do it
        :return:
        """
        if self.app.pargs.download is None:
            download_type = []
        else:
            download_type = self.app.pargs.download.split(',')  # type: list
            download_type = list(filter(lambda x: x in all_download_type, download_type))
        return download_type

    def param_check(self, params, func_name):
        """
        this will check param inputted and require is complete or not, and print help
        help will be in expose(help='...'), and got by function name
        :param params:
        :param func_name:
        :return:
        """
        help = None
        fun = getattr(self, func_name, None)
        if fun and getattr(fun, '__cement_meta__', None):
            help = fun.__cement_meta__['help']

        for p in params:
            param = getattr(self.app.pargs, p, None)
            if param is None:
                log.print_err("param {} miss, see help:".format(p))
                if help:
                    print(help)
                return False
        return True
