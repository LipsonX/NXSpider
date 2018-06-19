#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/4/19.
# email to LipsonChan@yahoo.com
#
import json
import os

from NXSpider.common import log
from NXSpider.common.constant import config_path, default_download_dir
from NXSpider.common.singleton import Singleton

default_path_key = 'default'
mv_resolutions = [240, 480, 720, 1080]


def utf8_data_to_file(f, data):
    if hasattr(data, 'decode'):
        f.write(data.decode('utf-8'))
    else:
        f.write(data)


class Config(Singleton):
    def __init__(self):
        if hasattr(self, '_init'):
            return
        self._init = True
        self.config_file_path = config_path

        # the deep level must be less than 2
        self.default_config = {
            'mongo': {
                'name': 'nxspider',
                'host': 'localhost',
                'port': 27017,
                'username': 'None',
                'password': 'None',
            },
            'download_path': [default_download_dir],
            'mv_def_resolution': 720,
            'media_tag': True,
            'media_tag_163': True,
            'download_file_check': True,
            'debug_log': True,
        }
        self.config = {}

        need_save = False
        try:
            f = open(self.config_file_path, 'r')
            self.config = json.loads(f.read())
            f.close()
        except IOError or ValueError:
            self.__generate_config_file()
            need_save = True

        # merge default
        for k, v in self.default_config.items():
            if k not in self.config:
                self.config[k] = v
                need_save = True

        paths = self.config['download_path']  # type: list
        if len(paths) == 0:
            paths.append(default_download_dir)
            need_save = True

        if need_save:
            self.save_config_file()

    def __getitem__(self, key):
        if key in self.config:
            return self.config[key]
        return None

    def __generate_config_file(self):
        f = open(self.config_file_path, 'w')
        utf8_data_to_file(f, json.dumps(self.default_config, indent=2))
        f.close()

    def save_config_file(self):
        f = open(self.config_file_path, 'w')
        utf8_data_to_file(f, json.dumps(self.config, indent=2))
        f.close()

    def get_mongo(self):
        return self.config['mongo']

    def get_path(self):
        return self.config['download_path'][0]

    def get_paths(self):
        return self.config['download_path']

    def get_mv_resolution(self):
        return self.config['mv_def_resolution']

    def get_media_tag(self):
        return self.config['media_tag']

    def get_media_tag_163(self):
        return self.config['media_tag_163']

    def get_file_check(self):
        return self.config['download_file_check']

    def save_config_dict(self, obj):
        """
        :type obj: dict
        :param obj:
        :return:
        """
        for k, v in obj.items():
            if isinstance(v, dict) and isinstance(self.config[k], dict):
                self.config[k].update(v)
            else:
                self.config[k] = v

    def config_test(self):
        result = True
        try:

            # check mongodb config
            mongo = self.config['mongo']
            for k in ['name', 'host', 'port']:
                if k not in mongo:
                    log.print_err("mongo config error, key mongo.{} is not set yet".format(k))
                    result = False

            # try import model, which will connect to server and exit if server config wrong
            import NXSpider.model.mongo_model

            for k in ['download_path', 'mv_def_resolution', 'media_tag', 'media_tag_163']:
                if k not in self.config:
                    log.print_err("config error, key {} is not set yet".format(k))
                    result = False

            # check type
            type_check = {
                'download_path': list,
                'mv_def_resolution': int,
                'media_tag': bool,
                'media_tag_163': bool,
                'download_file_check': bool,
            }

            need_save = False
            for k, v in type_check:
                if not isinstance(self.config[k], list):
                    log.print_err("config error, {} is not a require type, "
                                  "and is reset to default value: {}".format(k, self.default_config[k]))
                    self.config[k] = self.default_config[k]
                    need_save = True
                    result = False

            # download path check
            final_paths = []
            for p in self.config['download_path']:
                try:
                    # some error need pass
                    if os.path.isdir(p) is False:
                        os.mkdir(p)
                    final_paths.append(p)
                except:
                    log.print_warn("download path may be wrong and be deleted: {}".format(p))
                    need_save = True
                    result = False
                    pass

            # mv resolution check
            if self.config['mv_def_resolution'] not in mv_resolutions:
                log.print_warn("mv_def_resolution will be reset to default: {}"
                               .format(self.default_config['mv_def_resolution']))
                self.config['mv_def_resolution'] = self.default_config['mv_def_resolution']
                need_save = True
                result = False

            if need_save:
                self.config['download_path'] = final_paths
                self.save_config_file()

            return result
        except Exception as e:
            log.print_err(e)

        return False

    def config_reset(self):
        self.config = self.default_config
        self.save_config_file()
