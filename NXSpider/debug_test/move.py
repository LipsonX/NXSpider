#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/5/14.
# email to LipsonChan@yahoo.com
#
import os
import shutil
import sys
from glob import glob

# reload(sys)
# sys.setdefaultencoding('utf8')

paths = ['mv', 'mp3']
project_path = os.path.dirname(os.path.realpath(__file__))
project_path = os.path.dirname(project_path)
download_path = os.path.join(project_path, 'download_files')


def move_file(path):
    files = os.listdir(path)
    for f in files:
        if os.path.isdir(os.path.join(path, f)):
            continue

        author = f[0: f.find(' - ')].strip()
        author_path = os.path.join(path, author)
        if not os.path.exists(author_path):
            os.makedirs(author_path)
        shutil.move(os.path.join(path, f), os.path.join(author_path, f))


for p in paths:
    move_file(os.path.join(download_path, p))
