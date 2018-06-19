#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/4/20.
# email to LipsonChan@yahoo.com
#
import os
import re
from functools import reduce

from NXSpider.common.config import Config
from NXSpider.model.mongo_model import Mp4Model
from NXSpider.spider.api import get_mv_link
from NXSpider.spider.artist import Artist
from NXSpider.spider.base_driver import Music163Obj


def get_target_r(obj, limit_r=Config().get_mv_resolution()):
    max_valid = max([x['br'] for x in obj['brs']])
    return limit_r if max_valid > limit_r else max_valid


class MV(Music163Obj):
    __model_name__ = Mp4Model
    __model_rfilter__ = {
    }
    __parse_recursion__ = {
        'artists': Artist(),
    }

    def download_filename_format(self, doc):
        """
        implement pls
        get a path to save file, by relative path
        need be complete by child
        :param doc:
        :return:
        :rtype: str
        """
        authors = reduce(lambda x, y: x + ',' + y, [x['name'] for x in doc.artists])
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
            return get_mv_link(doc['id'], target_r)
        except:
            return None
