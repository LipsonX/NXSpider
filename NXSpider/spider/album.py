#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/4/26.
# email to LipsonChan@yahoo.com
#

from NXSpider.model.mongo_model import AlbumModel
from NXSpider.spider.artist import Artist
from NXSpider.spider.base_driver import Music163Obj, attr_replace


class Album(Music163Obj):
    __model_name__ = AlbumModel
    __model_rfilter__ = {
        # 'song',  # TODO need delete???
        'artist',
    }
    __parse_recursion__ = {
        'artists': Artist(),
    }

    @attr_replace(attr_name='songs', new_name='mp3')
    def replace_song(self, obj):
        return obj
