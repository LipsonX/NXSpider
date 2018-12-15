#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/4/19.
# email to LipsonChan@yahoo.com
#
from datetime import datetime

import pymongo
from mongoengine import connect, DynamicDocument, Document, signals
from mongoengine.fields import *
from pymongo.errors import ServerSelectionTimeoutError

from NXSpider.common import log
from NXSpider.common.config import Config
mongodb_conf = Config().get_mongo()

try:

    client = pymongo.MongoClient(host=mongodb_conf['host'],
                                 port=mongodb_conf['port'],
                                 connectTimeoutMS=3000,
                                 serverSelectionTimeoutMS=3000)
    test_connect = client.database.test.count()
    del client
except ServerSelectionTimeoutError as e:
    log.print_err("mongodb server config error")
    exit()

model_download_url = 'download_url'
model_is_download = 'downloaded'


def field_value(field, value):
    """
    Converts a supplied value to the type required by the field.
    If the field requires a EmbeddedDocument the EmbeddedDocument
    is created and updated using the supplied data.
    :param field:
    :param value:
    :return:
    """
    if field.__class__ in (ListField, SortedListField):
        # return a list of the field values
        return [
            field_value(field.field, item)
            for item in value]

    elif field.__class__ in (
            EmbeddedDocumentField,
            GenericEmbeddedDocumentField,
            ReferenceField,
            GenericReferenceField,
            LazyReferenceField):

        if isinstance(value, Document):
            return value

        if isinstance(value, dict):
            embedded_doc = field.document_type()
            update_doc(embedded_doc, value)
            return embedded_doc
        return None
    else:
        return value


def update_doc(doc, data):
    """
    Update an document to match the supplied dictionary.
    :param doc:
    :param data:
    :return:
    """

    for key, value in data.items():
        if hasattr(doc, key):
            value = field_value(doc._fields[key], value)
            setattr(doc, key, value)
        else:
            # handle invalid key
            pass

    return doc


def update_doc_filter(doc, filter_set, *dicts):
    """
    update document by filter and dicts
    :param doc:
    :param filter_set: Set
    :param dicts:
    :return:
    """
    obj = {}
    for d in dicts:
        obj.update({k: v for k, v in d.items() if k in filter_set})

    return update_doc(doc, obj)


def update_dynamic_doc(doc, data):
    for key, value in data.items():
        if key in doc._fields:
            value = field_value(doc._fields[key], value)
        setattr(doc, key, value)


def update_dynamic_doc_filter(doc, filter_set, *dicts):
    """
    update document by filter and dicts
    :param doc:
    :param filter_set: Set
    :param dicts:
    :return:
    """
    obj = {}
    for d in dicts:
        obj.update({k: v for k, v in d.items() if k in filter_set})

    return update_dynamic_doc(doc, obj)


def update_dynamic_doc_filter(doc, filter_set, *dicts):
    """
    update document by filter and dicts
    :param doc:
    :param filter_set: Set
    :param dicts:
    :type dicts: dict
    :type filter_set: list
    :return:
    :rtype: DynamicDocument | None
    """
    obj = {}
    for d in dicts:
        obj.update({k: v for k, v in d.items() if k in filter_set})

    return update_dynamic_doc(doc, obj)


def update_dynamic_doc_rfilter(doc, rfilter_set, *dicts):
    """
    update document by filter and dicts
    :param doc:
    :param rfilter_set: Set
    :param dicts:
    :type dicts: dict
    :type rfilter_set: Set
    :return:
    :rtype: DynamicDocument | None
    """
    rfilter_set = {} if rfilter_set is None else rfilter_set
    obj = {}
    for d in dicts:
        obj.update({k: v for k, v in d.items() if k not in rfilter_set})

    return update_dynamic_doc(doc, obj)


def get_one_model_by_key(model, model_id):
    """
    load or create a model by id
    :type model: DynamicDocument
    :param model:
    :param model_id:
    :return: doc, is_new
    :rtype: (DynamicDocument, boolean)
    """

    try:
        res = model.objects(id=model_id).first()
        if res is None:
            res = model(id=model_id)
            return res, True
        return res, False
    except Exception as e:
        log.print_err('load a doc err: %s' % e)
        return None, True


def update_dynamic_doc(doc, data):
    for key, value in data.items():
        if key in doc._fields:
            value = field_value(doc._fields[key], value)
        setattr(doc, key, value)


class ConfigModel(DynamicDocument):
    id = StringField(primary_key=True)
    updated_at = DateTimeField(default=datetime.utcnow)
    pass


class AuthorModel(DynamicDocument):
    id = LongField(primary_key=True)
    updated_at = DateTimeField(default=datetime.utcnow)
    pass


class Mp3Model(DynamicDocument):
    id = LongField(primary_key=True)
    artists = ListField(ReferenceField('ArtistModel'))
    album = ReferenceField('AlbumModel')
    mv = ReferenceField('Mp4Model')
    updated_at = DateTimeField(default=datetime.utcnow)
    pass


class ArtistModel(DynamicDocument):
    id = LongField(primary_key=True)
    # mp3s = ListField(ReferenceField(Mp3Model))
    updated_at = DateTimeField(default=datetime.utcnow)


class Mp4Model(DynamicDocument):
    id = LongField(primary_key=True)
    artists = ListField(ReferenceField(ArtistModel))
    updated_at = DateTimeField(default=datetime.utcnow)
    pass


class VideoModel(DynamicDocument):
    id = StringField(primary_key=True)
    artists = ListField(ReferenceField(ArtistModel))
    updated_at = DateTimeField(default=datetime.utcnow)
    pass


class PlaylistModel(DynamicDocument):
    id = LongField(primary_key=True)
    mp3s = ListField(LazyReferenceField(Mp3Model))
    mp4s = ListField(LazyReferenceField(Mp4Model))
    updated_at = DateTimeField(default=datetime.utcnow)


class AlbumModel(DynamicDocument):
    id = LongField(primary_key=True)
    mp3s = ListField(LazyReferenceField(Mp3Model))
    artists = ListField(LazyReferenceField(ArtistModel))
    updated_at = DateTimeField(default=datetime.utcnow)


class UserModel(DynamicDocument):
    id = LongField(primary_key=True)
    # friends = ListField(ReferenceField('self'))
    updated_at = DateTimeField(default=datetime.utcnow)


class Downloaded(DynamicDocument):
    model = StringField(required=True)
    model_id = LongField(required=True)
    updated_at = DateTimeField(default=datetime.utcnow)


def update_timestamp(sender, document, **kwargs):
    document.updated_at = datetime.utcnow()


signals.pre_save.connect(update_timestamp, sender=PlaylistModel)
signals.pre_save.connect(update_timestamp, sender=VideoModel)
signals.pre_save.connect(update_timestamp, sender=Mp4Model)
signals.pre_save.connect(update_timestamp, sender=Mp3Model)
signals.pre_save.connect(update_timestamp, sender=AuthorModel)
signals.pre_save.connect(update_timestamp, sender=ConfigModel)
signals.pre_save.connect(update_timestamp, sender=UserModel)
signals.pre_save.connect(update_timestamp, sender=ArtistModel)
signals.pre_save.connect(update_timestamp, sender=AlbumModel)

connect(mongodb_conf['name'], host=mongodb_conf['host'],
        port=mongodb_conf['port'], connectTimeoutMS=3000)
