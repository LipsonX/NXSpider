#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/4/19.
# email to LipsonChan@yahoo.com
#

from colorama import Fore
from colorama import init
init(autoreset=True)


def print_err(msg):
    print(Fore.RED + "ERROR: " + msg)


def print_warn(msg):
    print(Fore.YELLOW + "WARNING: " + msg)


def print_info(msg):
    print(Fore.BLUE + "INFO: " + msg)
