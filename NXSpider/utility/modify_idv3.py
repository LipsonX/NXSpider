#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/5/17.
# email to LipsonChan@yahoo.com
#
import os
import shutil

from NXSpider.common.config import Config
from NXSpider.model.mongo_model import Mp3Model, Mp4Model
from NXSpider.spider.mp3 import Mp3
from NXSpider.spider.mv import MV
from NXSpider.common import tools, log, constant
from NXSpider.spider.base_driver import Music163Obj
from NXSpider.utility.media_tag import attach_media_tag

media_types = {
    'mp3': [Mp3Model, Mp3],
    'mp4': [Mp4Model, MV],
}
paths = Config().get_paths()


def attach_media_idv3_by_db():
    """
    attach media idv3 by paths in config
    :return:
    """
    for suffix, type_setting in media_types:
        model, driver = type_setting    # type: Mp3Model or Mp4Model, Music163Obj
        objs = model.objects(downloaded=True)
        for obj in objs:
            file_path = driver.download_check(obj, check_file=True)
            if not file_path:
                continue

            if is_latin1(file_path):
                res = attach_media_tag(obj, file_path)
            else:
                res = attach_shadow(file_path, suffix, obj)

            log.print_info('idv3 attach %s, file: %s'
                           % ('success' if res else 'failed', file_path))


@tools.ignored(Exception)
def load_media_obj(media_type, download_name):
    return media_types[media_type][0].objects(download_file_name=download_name).first()


def create_tmp_dir():
    path = os.path.join(constant.main_dir, 'tmp')
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def delete_tmp_dir():
    path = os.path.join(constant.main_dir, 'tmp')
    if os.path.exists(path):
        os.removedirs(path)


def is_latin1(s):
    try:
        s.encode("iso-8859-1")
        return True
    except UnicodeEncodeError:
        return False


def attach_media_tag_by_path(path):
    """
    please run in python3 if your os is windows, cause os.walk has a encoding bug
    :type path: str
    :param path:
    :return:
    """

    for root, dirs, files in os.walk(path):
        for file in files:  # type: str
            suffix_i = file.rfind('.')
            suffix = file[suffix_i + 1:]
            if suffix not in media_types:
                continue

            split_txt = ' - '
            split_i = file.find(split_txt)
            if split_i == -1:
                continue

            artist = file[:split_i]
            download_file_name = os.path.join(artist, file)
            obj = load_media_obj(suffix, download_file_name)
            file_path = os.path.join(root, file)

            # fuck!!!! although i fix python-magic encoding bug of Chinese str in windows,
            # the fuck libmagic.dll doesn't recognize Korean. so, i am really pissed off to
            # change file name and change back
            '''
            if is_latin1(file_path):
                res = attach_media_tag(obj, file_path)
            else:
                res = attach_shadow(file_path, suffix, obj)
            '''

            # Dobby is free, thanks to mutagen
            res = attach_media_tag(obj, file_path)

            log.print_info('idv3 attach %s, file: %s'
                           % ('success' if res else 'failed', file_path))


def attach_shadow(file, suffix, obj):
    tmp_name = 'abc'
    tmp_file = os.path.join(create_tmp_dir(), tmp_name + '.' + suffix)
    shutil.copy(file, tmp_file)
    res = attach_media_tag(obj, tmp_file)
    if res:
        os.remove(file)
        shutil.copy(tmp_file, file)
    os.remove(tmp_file)
    return res


def attach_media_tag_by_conf_path():
    for path in paths:
        attach_media_tag_by_path(path)


