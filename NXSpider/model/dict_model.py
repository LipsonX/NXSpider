#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/4/19.
# email to LipsonChan@yahoo.com
#


class BaseDoc(dict):
    def save(self):
        pass

    def __getattr__(self, item):
        if item not in self:
            return None

        value = self[item]
        if isinstance(value, dict):
            value = BaseDoc(value)
        return value


def get_one_model_by_key(model, model_id):
    """
    load or create a model by id
    :param model:
    :param model_id:
    :return: doc, is_new
    :rtype: (DynamicDocument, boolean)
    """

    return model(id=model_id), True


def update_dynamic_doc(doc, data):
    """
    :type doc: dict
    :type data: dict
    :param doc:
    :param data:
    :return:
    """
    doc.update(data)


class ConfigModel(BaseDoc):
    pass


class AuthorModel(BaseDoc):
    pass


class Mp3Model(BaseDoc):
    pass


class ArtistModel(BaseDoc):
    pass


class Mp4Model(BaseDoc):
    pass


class VideoModel(BaseDoc):
    pass


class PlaylistModel(BaseDoc):
    pass


class AlbumModel(BaseDoc):
    pass


class UserModel(BaseDoc):
    pass


class Downloaded(BaseDoc):
    pass
