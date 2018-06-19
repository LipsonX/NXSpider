#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/6/5.
# email to LipsonChan@yahoo.com
#
import datetime

from cement.core.controller import CementBaseController, expose
from cement.core.foundation import CementApp

from NXSpider.bin.config_ctrl import ConfigController
from NXSpider import version
from colorama import init

from NXSpider.bin.spider_ctrl import SpiderController
from NXSpider.common.config import Config

BANNER = """
{} Application v{}
Copyright (c) {} {}
""".format(version.__title__, version.__version__ ,
           version.__author__, datetime.datetime.now().year)

init(autoreset=True)

class VersionController(CementBaseController):
    class Meta:
        label = 'base'
        description = ''
        arguments = [
            (['-v', '--version'], dict(action='version', version=BANNER)),
        ]


class App(CementApp):
    class Meta:
        label = "NXSpider"
        base_controller = "base"
        handlers = [VersionController, ConfigController, SpiderController]


def main():
    with App() as app:
        app.run()

if __name__ == "__main__":
    main()
