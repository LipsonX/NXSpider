#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/4/20.
# email to LipsonChan@yahoo.com
#

from NXSpider.spider.mp3 import Mp3
from NXSpider.spider.base_driver import *
from NXSpider.spider.user import User


class Playlist(Music163Obj):
    __model_name__ = PlaylistModel
    __model_rfilter__ = {
        # garbage properties
        'coverImgId_str',
        'coverImgId_str',
    }
    __parse_recursion__ = {
        'mp3': Mp3(),
        'creator': User(),
    }

    @attr_replace(attr_name='tracks', new_name='mp3')
    def replace_tracks(self, obj):
        return obj

    @attr_replace(attr_name='creator', new_name='creator')
    def replace_creator(self, obj):
        if 'userId' in obj and 'id' not in obj:
            obj['id'] = obj['userId']
        return obj
