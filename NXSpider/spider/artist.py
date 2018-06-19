#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/4/26.
# email to LipsonChan@yahoo.com
#

from NXSpider.model.mongo_model import ArtistModel
from NXSpider.spider.base_driver import Music163Obj


class Artist(Music163Obj):
    __model_name__ = ArtistModel
    __model_rfilter__ = {
        'img1v1Id',
        'picId',
    }
