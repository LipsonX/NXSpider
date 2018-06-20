#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/4/25.
# email to LipsonChan@yahoo.com
#
import codecs
import json
import os
from inspect import isfunction

import requests
import six
from mongoengine import DynamicDocument

from NXSpider.common.config import Config
from NXSpider.common import tools, log
from NXSpider.utility.media_tag import attach_media_tag
from NXSpider.model.export import *
import NXSpider.model.export


class Music163ObjException(Exception):
    pass


class Music163ObjMetaClass(type):
    def __new__(mcs, name, bases, attrs):
        """
        :param name:
        :type name: str
        :param bases:
        :param attrs:
        :type attrs: dict
        :return:
        """
        if name == "Music163Obj":
            return type.__new__(mcs, name, bases, attrs)
        if '__model_name__' not in attrs or attrs['__model_name__'] is None:
            attrs['__model_name__'] = name + "Model"

        # set download level 1 path
        attrs['__file_type__'] = name.lower()

        # create download file dir for download path
        # obj_path = os.path.join(get_download_path(), attrs['__file_type__'])
        # if not os.path.exists(obj_path):
        #     os.makedirs(obj_path)

        # create a empty dict
        attrs['__attrs_replace_fucs__'] = dict()
        attrs['__attrs_replace_map__'] = dict()

        # set replace
        replace_map = dict()
        for k, v in attrs.items():
            if isfunction(v):
                if getattr(v, '__attrs_replace__', False):
                    org_name = getattr(v, '__attrs_replace_org__')
                    replace_map[org_name] = getattr(v, '__attrs_replace_new__')
                    attrs['__attrs_replace_fucs__'][org_name] = v
        attrs['__attrs_replace_map__'] = replace_map
        return type.__new__(mcs, name, bases, attrs)


def attr_replace(attr_name=None, new_name=None):
    """
    replace attr value
    decorator for fun: (self, obj)->object

    :param new_name:
    :param attr_name:
    :return:
    """

    def de(f):
        """
        :type f: function
        :param f:
        :return:
        """
        f.__attrs_replace__ = True
        def_name = f.__name__
        f.__attrs_replace_org__ = attr_name if attr_name else def_name
        f.__attrs_replace_new__ = new_name if new_name else def_name
        return f

    return de


# class Music163Obj(object, metaclass=Music163ObjMetaClass):
class Music163Obj(six.with_metaclass(Music163ObjMetaClass)):
    __model_name__ = None
    __model_rfilter__ = set()
    __file_type__ = 'other'
    __parse_recursion__ = {}

    __attrs_replace_fucs__ = dict()
    __attrs_replace_map__ = dict()

    # __metaclass__ = Music163ObjMetaClass

    def __init__(self, *args, **kwargs):
        """
        In some case, something want to change def class setting,
        like recursion or filter
        :param args:
        :param kwargs:
        """
        for k, v in kwargs.items():
            if k in ['__parse_recursion__', '__model_rfilter__']:
                setattr(self, k, v)

    def download_filename_format(self, doc):
        """
        implement pls
        get a path to save file, by relative path
        need be complete by child
        :param doc:
        :return:
        :rtype: str
        """
        return None

    def url_load(self, doc):
        """
        implement pls
        :param doc:
        :return:
        :rtype: str
        """
        return None

    def pre_save(self, doc, obj):
        """
        implement pls, not force
        do something before doc save
        get download link here is better
        :param doc:
        :param obj:
        :return:
        """
        pass

    def request_file(self, doc):
        """
        implement pls
        :param doc:
        :return:
        :rtype: bytes
        """
        url = None
        try:
            url = getattr(doc, model_download_url, None)
            if url is None:
                return None

            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.content
        except Exception as e:
            log.print_info(u"url download failed %s , err: %s" % (url, e))
            return None

    def download_relative_path(self, doc):
        download_file_name = 'download_file_name'
        if download_file_name not in doc:
            doc[download_file_name] = self.download_filename_format(doc)
        filename = doc[download_file_name]
        if filename:
            return os.path.join(self.__file_type__, filename)
        else:
            return None

    def download_check(self, doc, check_file=False):
        """
        :param doc:
        :param check_file: check dist file to download
        :type doc: DynamicDocument
        :return:
        """
        if check_file:
            file_relative_path = self.download_relative_path(doc)
            for path in Config().get_paths():
                file_path = os.path.join(path, file_relative_path)
                if os.path.exists(file_path):
                    self.download_log(doc)
                    return file_path
            self.download_log(doc, downloaded=False)
            return False

        return hasattr(doc, model_is_download) and doc[model_is_download]

    def download_log(self, doc, downloaded=True):
        doc[model_is_download] = downloaded

    def download_file_tag(self, filename, doc):
        if self.__file_type__ in ['mp3', 'mp4', 'mv'] \
                and Config().get_media_tag():
            attach_media_tag(doc, filename)

    def download_file(self, doc):
        """
        download file from music 163
        :param doc:
        :return:
        """
        file_relative_path = self.download_relative_path(doc)
        path = Config().get_path()
        content = self.request_file(doc)

        if content is None:
            log.print_err(u"file download failed : %s" % file_relative_path)
            return False

        try:
            file_name = os.path.join(path, file_relative_path)

            # dir make
            dir_name = os.path.dirname(file_name)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)

            # file write
            with open(file_name, "wb") as code:
                code.write(content)

            self.download_file_tag(file_name, doc)

            log.print_info(u"file download complete: %s" % file_relative_path)
            self.download_log(doc)
            return True
        except Exception as e:
            log.print_err("file save failed : %s, err: %s" % (file_relative_path, e))
            return False

    def debug_save_json(self, obj):
        with tools.ignored(Exception):
            relative_path = os.path.join(self.__file_type__ + '.debug',
                                         self.__file_type__ + "_" +
                                         str(obj['id']) + '.json')
            file_name = os.path.join(Config().get_path(), relative_path)
            with codecs.open(file_name, "wb", encoding='utf8') as code:
                test = json.dumps(obj, ensure_ascii=False)
                code.write(test)

    def debug_print(self, obj):
        msg = u"spider {} complete, id: {}".format(self.__file_type__, obj['id'])
        if 'name' in obj:
            msg += u", name: {}".format(obj['name'])

        log.print_info(msg)

    def parse_new_model(self, doc, obj):
        pass

    def try_download(self, doc, download_type, file_check):
        if self.__file_type__ not in download_type:
            return True

        # download file and set download flag
        if download_type is not None \
                and not self.download_check(doc, check_file=file_check):
            # need download， try url which is set first or get new url and download
            if getattr(doc, model_download_url, None) \
                    and self.download_file(doc):
                return True

            # get download link here
            doc[model_download_url] = self.url_load(doc)
            self.download_file(doc)
        else:
            name = self.download_relative_path(doc)
            if name:
                log.print_info(u"file is exist or is not need to download : %s"
                               % name)

    def parse_model(self, crawl_dict, download_type=None,
                    file_check=False, save=True, debug=False):
        """
        Get a model from db or create, update and save!!!
        this will replace some attributes into models by load_save_model also.
        by @attr_replace(attr_name, new_name)
        :param debug:
        :param file_check:
        :param download_type:
        :param save: save doc
        :param crawl_dict: must have id attr
        :type crawl_dict: dict
        :return:
        :rtype: DynamicDocument
        :type save: bool
        """
        if debug:
            # self.debug_save_json(crawl_dict)
            pass

        # get id
        if 'id' not in crawl_dict:
            log.print_err(u"can not load id by json obj %s" % json.dumps(crawl_dict))
            return None
        doc_id = crawl_dict['id']

        # load a mongo document
        doc, is_new_doc = get_one_model_by_key(self.__model_name__, doc_id)
        if doc is None:
            log.print_err(u"can not load a doc by obj %s_%d"
                          % (self.__file_type__, doc_id))
            return None

        # if is_new_doc:
        # replace attr or ignore
        obj = dict()
        for k, v in crawl_dict.items():
            if k in self.__model_rfilter__:
                continue
            obj[k] = v

            # replace object
            if k not in self.__attrs_replace_fucs__:
                continue

            # change attr
            if isinstance(v, list):
                v = [self.__attrs_replace_fucs__[k](self, x) for x in v]
            else:
                v = self.__attrs_replace_fucs__[k](self, v)

            # replace key name
            del obj[k]
            obj[self.__attrs_replace_map__[k]] = v

        # recursion replace a attr into a model
        for k, v in self.__parse_recursion__.items():
            if k not in obj:
                continue

            if isinstance(obj[k], list):
                obj[k] = [v.parse_model(x, save=save, download_type=download_type,
                                        file_check=file_check, debug=debug) for x in obj[k]]
            elif isinstance(obj[k], dict):
                obj[k] = v.parse_model(obj[k], save=save, download_type=download_type,
                                       file_check=file_check, debug=debug)

        # update json to doc, this must be after recursion
        update_dynamic_doc(doc, obj)

        # modify doc and
        self.pre_save(doc, crawl_dict)

        # try download
        self.try_download(doc, download_type, file_check)

        # save document
        if isinstance(doc, DynamicDocument) and save:
            doc.save()

        if debug:
            self.debug_print(crawl_dict)

        return doc


__all__ = [
    'Music163Obj',
    'attr_replace',
    'Music163ObjException',

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
