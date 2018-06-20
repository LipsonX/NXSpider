#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/6/5.
# email to LipsonChan@yahoo.com
#
import json
import os

from cement.core.controller import CementBaseController, expose

from NXSpider.common import log
from NXSpider.common.config import Config, default_path_key, mv_resolutions
from NXSpider.common.constant import default_download_dir


class ConfigController(CementBaseController):
    class Meta:
        label = "config"
        stacked_on = 'base'
        description = "NXSpider config"
        arguments = [
            (['-mh', '--mhost'],
             dict(help="mongo host")),
            (['-mp', '--mport'],
             dict(help="mongo port")),
            (['-mu', '--muser'],
             dict(help="mongo user")),
            (['-mpw', '--mpassword'],
             dict(help="mongo password")),
            (['-mn', '--mdbname'],
             dict(help="mongo db name, default nxspider")),
            (['-nomongo', '--nomongo'],
             dict(help="no mongo mode, true(1) or false(0), default True, while true, mongodb will be never used")),

            (['-path', '--path_download'],
             dict(help="download path, default ~/.nxspider/download_files/, eg. -path defualt;path1;path2")),
            (['-mvr', '--mv_resolution'],
             dict(help="mv default resolution, [240, 480, 720, 1080] default 720")),
            (['-tag', '--media_tag'],
             dict(help="media tag, true(1) or false(0), default True")),
            (['-tag163', '--media_tag_163'],
             dict(help="media tag of 163 comment, true(1) or false(0), default True")),
            (['-dfc', '--download_file_check'],
             dict(help="check file exist in paths set, true(1) or false(0), default True")),
        ]

    @expose(help="config mongo server with [-h --host] [-p --port] "
                 "[-u --user] [-pw --password] [-c --collections]")
    def config_mongo(self):
        config = Config()
        config_dict = config.config  # type: dict
        mongo_key = 'mongo'
        is_config = False
        try:
            if self.app.pargs.mhost is not None:
                config_dict[mongo_key]['host'] = self.app.pargs.mhost
                config_dict['no_mongo'] = False
                is_config = True

            if self.app.pargs.mport is not None:
                config_dict[mongo_key]['port'] = int(self.app.pargs.mport)
                is_config = True

            if self.app.pargs.muser is not None:
                config_dict[mongo_key]['username'] = self.app.pargs.muser
                is_config = True

            if self.app.pargs.mpassword is not None:
                config_dict[mongo_key]['password'] = self.app.pargs.mpassword
                is_config = True

            if self.app.pargs.mdbname is not None:
                config_dict[mongo_key]['name'] = self.app.pargs.mdbname
                is_config = True

            if self.app.pargs.nomongo is not None:
                config_dict['no_mongo'] = True if self.app.pargs.nomongo.lower() == 'true'\
                                                   or self.app.pargs.nomongo == '1' else False
        except:
            log.print_err("input error, pls check")
            raise
        if is_config:
            config.save_config_file()
        log.print_info("config success")
        self.config_show()

    @expose(help="config spider behavior with [-path <defualt,path1,path2>]"
                 "[-mvr <240,480,720,1080>] [-tag <1 or 0>] [-tag163 <1 or 0>]"
                 "[-dfc <1 or 0>]")
    def config_spider(self):
        config = Config()
        config_dict = config.config  # type: dict
        is_config = False
        try:
            if self.app.pargs.path_download is not None:
                paths = self.app.pargs.path_download.split(',')  # type: list
                if default_path_key in paths:
                    index = paths.index(default_path_key)
                    paths.remove(default_path_key)
                    paths.insert(index, default_download_dir)

                final_paths = []
                for p in paths:
                    try:
                        # some error need pass
                        if os.path.isdir(p) is False:
                            os.mkdir(p)
                        final_paths.append(p)
                    except:
                        log.print_warn("path may be wrong and be deleted: {}".format(p))
                        pass

                if not final_paths:
                    final_paths.append(default_download_dir)

                log.print_info('path will be set as: ' + ','.join(final_paths))

                config_dict['download_path'] = final_paths
                is_config = True

            if self.app.pargs.mv_resolution is not None:
                r = int(self.app.pargs.mv_resolution)
                if r not in mv_resolutions:
                    log.print_warn("-mvr resolution config skip, value must be 240,480,720,1080")
                config_dict['mv_def_resolution'] = r
                is_config = True

            if self.app.pargs.media_tag is not None:
                config_dict['media_tag'] = True if self.app.pargs.media_tag.lower() == 'true'\
                                                   or self.app.pargs.media_tag == '1' else False
                is_config = True

            if self.app.pargs.media_tag_163 is not None:
                config_dict['media_tag_163'] = True if self.app.pargs.media_tag_163.lower() == 'true' \
                                                       or self.app.pargs.media_tag_163 == '1' else False
                is_config = True

        except:
            log.print_err("input error, pls check")
            raise
        if is_config:
            config.save_config_file()
        log.print_info("config success")
        self.config_show()

    @expose(help="check config is valid or not")
    def config_check(self):
        self.config_show()
        try:
            config = Config()
            if config.config_test():
                log.print_info('config check complete, all is well done!')
        except:
            log.print_err('config check failed, pls re config')

    @expose(help="clear all config, u need re-config from beginning")
    def config_clear(self):
        Config().config_reset()
        log.print_info("config has been reset, u need re-config from beginning pls")
        self.config_show()

    @expose(help="list all config opt")
    def config_show(self):
        config_dict = Config().config
        log.print_info("config will be show fellow:")
        print(json.dumps(config_dict, ensure_ascii=False, indent=1))

