#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/6/19.
# email to LipsonChan@yahoo.com
#
import sys

from cement.core.controller import expose
from terminaltables import AsciiTable

from NXSpider.bin.base_ctrl import NXSpiderBaseController, py2_decoding
from NXSpider.bin.print_as_table import print_mp3s, print_playlist, print_users, print_albums, print_artists, print_mvs
from NXSpider.common import PYTHON2, log
from NXSpider.spider import api
from NXSpider.spider.api import search_types, PLAYLIST_CLASSES

PRINT_ATTR_FUNC_MAP = {
    'mp3': ['songs', print_mp3s],
    'playlist': ['playlists', print_playlist],
    'user': ['userprofiles', print_users],
    'artist': ['artists', print_artists],
    'album': ['albums', print_albums],
    'mv': ['mvs', print_mvs],
}


class ShowController(NXSpiderBaseController):
    class Meta:
        label = "show"
        stacked_on = 'base'
        description = "NXSpider"

    @expose(help="search [-ar <artist>] [-pl <playlist>] "
                 "[-ur <user>] [-mp3 <song>] [-ab <album>] [-mv <mv>]")
    def search(self):
        search_key = 'mp3'
        key_num = 0
        for k, v in search_types.items():
            if getattr(self.app.pargs, k, None):
                search_key = k
                key_num += 1
        if key_num > 1:
            log.print_err("it could search by only one type")

        # input must be decode in python2
        search_value = getattr(self.app.pargs, search_key)
        search_value = py2_decoding(search_value)

        res = api.search(search_value, stype=search_key,
                         offset=self.app.pargs.offset or 0,
                         limit=self.app.pargs.limit or 50)

        if not res:
            log.print_info("nothing found!")
            return

        if search_key in PRINT_ATTR_FUNC_MAP:
            func = PRINT_ATTR_FUNC_MAP[search_key][1]   # type: function
            value = (res.get(PRINT_ATTR_FUNC_MAP[search_key][0], []))   # type: list
            func(value)

    @expose(help="show artists ablum, usage: sw-ar-ab -ar <artist_id> [-offset <offset>] [-limit <limit>]")
    def sw_ar_ab(self):
        if self.param_check(['artist'], sys._getframe().f_code.co_name) is False:
            return

        artistid = self.app.pargs.artist  # type: list
        artist_detail = api.get_artist_album(artistid,
                                             offset=self.app.pargs.offset or 0,
                                             limit=self.app.pargs.limit or 50)

        print_albums(artist_detail['hotAlbums'])
        pass

    @expose(help="show user playlist, usage: sw-ur-pl -ur <user_id,id1,id2>")
    def sw_ur_pl(self):
        # todo
        pass

    @expose(help="show all playlist classes, usage: sw-pl-classes")
    def sw_pl_classes(self):
        table = AsciiTable([["Group", "Classes(which can be as a input)"]])
        table_data = [[k, ', '.join(v)] for k, v in PLAYLIST_CLASSES.items()]
        table.table_data.extend(table_data)
        print(table.table)
