#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/12/12.
# email to LipsonChan@yahoo.com
#

import os
import re

from NXSpider.common.config import Config
from NXSpider.spider.api import get_video_link
from NXSpider.spider.artist import Artist
from NXSpider.spider.base_driver import *


def get_target_r(obj, limit_r=Config().get_mv_resolution()):
    max_valid = max([x['resolution'] for x in obj['resolutions']])
    return limit_r if max_valid > limit_r else max_valid


class Video(Music163Obj):
    __model_name__ = VideoModel
    __model_rfilter__ = {
    }
    __parse_recursion__ = {
        'artists': Artist(),
    }

    def download_filename_full(self, doc):
        """
        implement pls
        get a path to save file, by relative path
        need be complete by child
        :param doc:
        :return:
        :rtype: str
        """
        # todo modify
        authors = ",".join([x['name'] for x in doc.artists])
        author = re.sub("[\\\\/:*?\"<>|]", '', authors.strip())
        mp3_name = re.sub("[\\\\/:*?\"<>|]", '', doc['name'])
        name = os.path.join(author, "%s - %s.mp4" % (author, mp3_name))
        return name

    def url_load(self, doc):
        """
        implement pls
        :param doc:
        :return:
        :rtype: str
        """
        try:
            target_r = get_target_r(doc, Config().get_mv_resolution())
            doc['download_video_r'] = target_r
            return get_video_link(doc['id'], target_r)
        except:
            return None
