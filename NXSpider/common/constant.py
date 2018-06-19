#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/5/30.
# email to LipsonChan@yahoo.com
#
import os

# version = '0.0.1'

all_download_type = ['mp3', 'mv']
main_dir = os.path.join(os.path.expanduser('~'), '.nxspider')
config_path = os.path.join(main_dir, 'config.json')
default_download_dir = os.path.join(main_dir, 'download_files')

if os.path.isdir(main_dir) is False:
    os.mkdir(main_dir)
