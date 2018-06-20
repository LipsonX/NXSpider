#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/6/20.
# email to LipsonChan@yahoo.com
#

from NXSpider.common.config import Config
if Config().get_has_mongo():
    from NXSpider.model.mongo_model import *
else:
    from NXSpider.model.dict_model import *

model_download_url = 'download_url'
model_is_download = 'downloaded'

__all__ = [
    'ConfigModel',
    'UserModel',
    'AlbumModel',
    'PlaylistModel',
    'Mp4Model',
    'ArtistModel',
    'Mp3Model',
    'AuthorModel',
    'update_dynamic_doc',
    'model_download_url',
    'model_is_download',
    'get_one_model_by_key',
]