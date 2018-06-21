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
from NXSpider.common import PYTHON2, log
from NXSpider.spider import api
from NXSpider.spider.api import search_types, PLAYLIST_CLASSES


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

        table = ''
        if search_key == 'mp3' and 'songs' in res:
            table = AsciiTable([["ID", "Name", "Album", "AlbumID", "Artist", "ArtistID"]])
            table_data = [[str(item['id']), item['name'],
                           item['album']['name'], item['album']['id'],
                           ','.join([ar['name'] for ar in item['artists']]),
                           ','.join([str(ar['id']) for ar in item['artists']]),
                           ] for item in res['songs']]
            table.table_data.extend(table_data)
        elif search_key == 'playlist' and 'playlists' in res:
            table = AsciiTable([["ID", "Name", "User", "PlayCount", "FavoriteCount"]])
            table_data = [[str(item['id']), item['name'],
                           item['creator']['nickname'],
                           str(item['playCount']),
                           str(item['bookCount']),
                           ] for item in res['playlists']]
            table.table_data.extend(table_data)
            pass
        elif search_key == 'user' and 'userprofiles' in res:
            table = AsciiTable([["ID", "Name", "Signature"]])
            table_data = [[str(item['userId']), item['nickname'],
                           item['signature'],
                           ] for item in res['userprofiles']]
            table.table_data.extend(table_data)
            pass
        elif search_key == 'artist' and 'artists' in res:
            table = AsciiTable([["ID", "Name", "AlbumNum", "MVNum"]])
            table_data = [[str(item['id']), item['name'],
                           str(item['albumSize']),
                           str(item['mvSize'])
                           ] for item in res['artists']]
            table.table_data.extend(table_data)
        elif search_key == 'album' and 'albums' in res:
            table = AsciiTable([["ID", "Album", "Artist", "ArtistID"]])
            table_data = [[str(item['id']), item['name'],
                           ','.join([ar['name'] for ar in item['artists']]),
                           ','.join([str(ar['id']) for ar in item['artists']]),
                           ] for item in res['albums']]
            table.table_data.extend(table_data)
            pass
        elif search_key == 'mv' and 'mvs' in res:
            table = AsciiTable([["ID", "Name", "Artist", "ArtistID", "Duration", "PlayCount"]])
            table_data = [[str(item['id']), item['name'],
                           item['artistName'],
                           item['artistId'],
                           '%02d:%02d' % divmod(int(item['duration'] / 1000), 60),
                           item['playCount'],
                           ] for item in res['mvs']]
            table.table_data.extend(table_data)
            pass

        if table == '':
            log.print_err('nothing found')
        else:
            print(table.table)

    @expose(help="show artists ablum, usage: sw-ar-ab -ar <artist_id> [-offset <offset>] [-limit <limit>]")
    def sw_ar_ab(self):
        if self.param_check(['artist'], sys._getframe().f_code.co_name) is False:
            return

        artistid = self.app.pargs.artist  # type: list
        artist_detail = api.get_artist_album(artistid,
                                             offset=self.app.pargs.offset or 0,
                                             limit=self.app.pargs.limit or 50)
        table = AsciiTable([["ID", "Name", "Artist", "Song", "Company"]])
        table_data = [[str(item['id']), item['name'],
                       item['artist']['name'], item['size'], item['company']
                       ] for item in artist_detail['hotAlbums']]
        table.table_data.extend(table_data)
        print(table.table)
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
