#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/4/23.
# email to LipsonChan@yahoo.com
#
import os
import re
from NXSpider.model.mongo_model import Mp3Model
from NXSpider.spider.album import Album
from NXSpider.spider.api import get_mp3_link, get_mv_detail
from NXSpider.spider.artist import Artist
from NXSpider.spider.mv import MV
from NXSpider.spider.base_driver import Music163Obj, attr_replace


class Mp3(Music163Obj):
    __model_name__ = Mp3Model
    __model_rfilter__ = {
        'artists',  # read from album model
    }
    __parse_recursion__ = {
        'artists': Artist(),
        'album': Album(__model_rfilter__={'artist','songs'}),
        'mv': MV(),
    }

    @attr_replace(attr_name='mvid', new_name='mv')
    def replace_mvid(self, obj):
        if obj != 0:
            obj = get_mv_detail(obj)
            return obj
        return None

    def pre_save(self, doc, obj):
        """
        :param doc:
        :param obj:
        :type doc: Mp3Model
        :return:
        """
        # set artists
        if getattr(doc, 'album', False) and getattr(doc['album'], 'artists', False):
            doc.artists = [a for a in doc['album']['artists']]

    def download_filename_format(self, doc):
        """
        implement pls
        get a path to save file, by relative path
        need be complete by child
        :param doc:
        :type doc: Mp3Model
        :return:
        :rtype: str
        """
        # authors = reduce(lambda x, y: x + ',' + y, [x['name'] for x in doc.artists])
        authors = ','.join([x['name'] for x in doc.artists])
        author = re.sub("[\\\\/:*?\"<>|]", '', authors.strip())
        mp3_name = re.sub("[\\\\/:*?\"<>|]", '', doc['name'])
        name = os.path.join(author, "%s - %s.mp3" % (author, mp3_name))
        return name

    def url_load(self, doc):
        """
        implement pls
        :param doc:
        :return:
        :rtype: str
        """
        try:
            return get_mp3_link(doc['id'])
        except:
            return None
