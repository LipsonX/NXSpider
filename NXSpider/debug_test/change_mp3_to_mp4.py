#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/5/15.
# email to LipsonChan@yahoo.com
#
import os
import shutil

paths = ['mv']
project_path = os.path.dirname(os.path.realpath(__file__))
project_path = os.path.dirname(project_path)
download_path = os.path.join(project_path, 'download_files')


def rename_file(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            f = f  # type: str
            suffix = f[f.rfind('.'):]
            if suffix == '.mp3':
                new_name = f[:f.rfind('.')] + ".mp4"
                os.rename(os.path.join(root, f), os.path.join(root, new_name))


for p in paths:
    rename_file(os.path.join(download_path, p))

