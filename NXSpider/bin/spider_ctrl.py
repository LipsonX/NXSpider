#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/6/6.
# email to LipsonChan@yahoo.com
#
import sys
from inspect import isfunction

from cement.core.controller import CementBaseController, expose
from terminaltables import AsciiTable

from NXSpider.common import log, tools, PYTHON2
from NXSpider.common.config import Config
from NXSpider.common.constant import all_download_type
from NXSpider.spider import api
from NXSpider.spider.api import search_types


class SpiderController(CementBaseController):
    class Meta:
        label = "spider"
        stacked_on = 'base'
        description = "NXSpider"
        arguments = [
            (['-ar', '--artist'],
             dict(help="artist")),
            (['-pl', '--playlist'],
             dict(help="playlist")),
            (['-ur', '--user'],
             dict(help="user")),
            (['-mv', '--mv'],
             dict(help="artist")),
            (['-mp3', '--mp3'],
             dict(help="song")),
            (['-ab', '--album'],
             dict(help="album")),
            (['-dw', '--download'],
             dict(help="download files, [<mv,mp3>], eg. -dw mv,mp3")),
            (['-offset'],
             dict(help="offset index, eg. -offset 50")),
            (['-limit'],
             dict(help="limit size, eg. -limit 50")),
        ]

    def parse_download(self):
        """
        lost of spider function will parse -dw param, this will do it
        :return:
        """
        if self.app.pargs.download is None:
            download_type = []
        else:
            download_type = self.app.pargs.download.split(',')  # type: list
            download_type = list(filter(lambda x: x in all_download_type, download_type))
        return download_type

    def param_check(self, params, func_name):
        """
        this will check param inputted and require is complete or not, and print help
        help will be in expose(help='...'), and got by function name
        :param params:
        :param func_name:
        :return:
        """
        help = None
        fun = getattr(self, func_name, None)
        if fun and getattr(fun, '__cement_meta__', None):
            help = fun.__cement_meta__['help']

        for p in params:
            param = getattr(self.app.pargs, p, None)
            if param is None:
                log.print_err("param {} miss, see help:". format(p))
                if help:
                    print(help)
                return False
        return True


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
        if PYTHON2:
            search_value = search_value.decode(sys.getfilesystemencoding())
            # print(sys.stdout.encoding)
            # print(sys.stdin.encoding)

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
            table = AsciiTable([["ID", "Name", "User", "PlayCount", "FavoriteCount", "ArtistID"]])
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
        # elif search_key == 'album':
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
                       ] for item in artist_detail]
        table.table_data.extend(table_data)
        print(table.table)
        pass

    @expose(help="show user playlist, usage: sw-ur-pl -ur <user_id,id1,id2>")
    def sw_ur_pl(self):
        # todo
        pass

    @expose(help="spider playlist, usage: spls -pl <playlist_id,id2,id3> [-dw <mv,mp3>] ")
    def spls(self):
        from NXSpider.bin.models import playlist_mo

        if self.param_check(['playlist'], sys._getframe().f_code.co_name) is False:
            return

        download_type = self.parse_download()
        playlists = self.app.pargs.playlist.split(',')  # type: list

        for pid in playlists:
            playlist_detail = api.get_playlist_detail(pid)
            if playlist_detail:
                log.print_info(u"<{}> author：{}".format(
                    playlist_detail['name'],
                    playlist_detail['creator']['nickname'],
                ))
                playlist_mo.parse_model(playlist_detail,
                                        download_type=download_type,
                                        file_check=Config().get_file_check())

        log.print_info("spider complete!~")
        pass

    @expose(help="spider artist top mp3, usage: sar_top_mp3 -ar <artist_id,id1,id2> [-dw <mv,mp3>]")
    def sar_top_mp3(self):
        from NXSpider.bin.models import artist_mo

        if self.param_check(['artist'], sys._getframe().f_code.co_name) is False:
            return

        download_type = self.parse_download()
        artists = self.app.pargs.artist.split(',')  # type: list

        for arid in artists:
            detail = api.get_artists_songs(arid)
            if detail is None:
                continue

            artist_detail = detail['artist']
            artist_detail['mp3'] = detail['hotSongs']

            log.print_info(u"<{}>".format(artist_detail['name']))
            artist_mo.parse_model(artist_detail,
                                 download_type=download_type,
                                 file_check=Config().get_file_check())

        log.print_info("spider complete!~")
        pass

    @expose(help="spider album, usage: sab -ab <album_id,id1,id2> [-dw <mv,mp3>]")
    def sab(self):
        from NXSpider.bin.models import album_mo

        if self.param_check(['album'], sys._getframe().f_code.co_name) is False:
            return

        download_type = self.parse_download()
        albums = self.app.pargs.album.split(',')  # type: list

        for pid in albums:
            album_detail = api.get_album_detail(pid)
            if album_detail is None:
                continue

            log.print_info(u"{} artist：{}".format(
                "<" + album_detail['name'] + ">",
                album_detail['artist']['name'],
            ))
            album_mo.parse_model(album_detail,
                                 download_type=download_type,
                                 file_check=Config().get_file_check())

        log.print_info("spider complete!~")
        pass
