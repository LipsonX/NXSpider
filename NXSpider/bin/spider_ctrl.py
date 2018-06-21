#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/6/6.
# email to LipsonChan@yahoo.com
#
import sys

from cement.core.controller import expose

from NXSpider.bin.base_ctrl import NXSpiderBaseController, py2_decoding, py2_encoding
from NXSpider.common import log
from NXSpider.common.config import Config
from NXSpider.spider import api


class SpiderController(NXSpiderBaseController):
    class Meta:
        label = "spider"
        stacked_on = 'base'
        description = "NXSpider"
        arguments = [
            (['-cls', '--cls'],
             dict(help="classes or catalogue")),
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

    @expose(
        help="spider playlist, usage: scls-pls -cls <class name> [-dw <mv,mp3>] [-offset <offset>] [-limit <limit>]")
    def scls_pls(self):
        from NXSpider.bin.models import playlist_mo

        if self.param_check(['cls'], sys._getframe().f_code.co_name) is False:
            return

        download_type = self.parse_download()
        class_name = self.app.pargs.cls
        class_name = py2_decoding(class_name)

        if class_name != u"全部" and py2_encoding(class_name) not in api.ALL_CLASSES:
            log.print_err("class name is wrong, pls check by run : nxspider sw-pl-classes")
            return

        playlists = api.get_top_playlists(category=class_name,
                                          offset=self.app.pargs.offset or 0,
                                          limit=self.app.pargs.limit or 50)  # type: list

        for pl_obj in playlists:
            playlist_detail = api.get_playlist_detail(pl_obj['id'])
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

    @expose(help="spider artist top mp3, usage: sar-top-mp3 -ar <artist_id,id1,id2> [-dw <mv,mp3>]")
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

    @expose(help="spider artist albums, usage: sar-albums -ar <artist_id,id1,id2> [-dw <mv,mp3>] "
                 "[-offset <offset>] [-limit <limit>]")
    def sar_albums(self):
        from NXSpider.bin.models import artist_album_mo

        if self.param_check(['artist'], sys._getframe().f_code.co_name) is False:
            return

        download_type = self.parse_download()
        artists = self.app.pargs.artist.split(',')  # type: list

        for arid in artists:
            detail = api.get_artist_album(arid,
                                          offset=self.app.pargs.offset or 0,
                                          limit=self.app.pargs.limit or 50)
            if detail is None:
                continue

            artist_detail = detail['artist']
            album_details = [api.get_album_detail(d['id']) for d in detail['hotAlbums']]
            album_details = [d for d in album_details if d]
            artist_detail['albums'] = album_details

            from terminaltables import AsciiTable
            table = AsciiTable([["ID", "Album", "Artist", "ArtistID"]])
            table_data = [[str(item['id']), item['name'],
                           ','.join([ar['name'] for ar in item['artists']]),
                           ','.join([str(ar['id']) for ar in item['artists']]),
                           ] for item in artist_detail['albums']]
            table.table_data.extend(table_data)

            log.print_info(u"<{}>".format(artist_detail['name']))
            log.print_info("albums bellow will be crawled")
            print(table.table)

            artist_album_mo.parse_model(artist_detail,
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

    @expose(
        help="spider playlist, usage: sur-pls -ur <user id,id1,id2> [-dw <mv,mp3>] [-offset <offset>] [-limit <limit>]")
    def sur_pls(self):
        from NXSpider.bin.models import playlist_mo

        if self.param_check(['user'], sys._getframe().f_code.co_name) is False:
            return

        download_type = self.parse_download()
        user_id = self.app.pargs.user
        playlists = api.user_playlist(user_id)

        from terminaltables import AsciiTable
        table = AsciiTable([["ID", "Name", "User", "PlayCount"]])
        table_data = [[str(item['id']), item['name'],
                       item['creator']['nickname'],
                       str(item['playCount']),
                       ] for item in playlists]
        table.table_data.extend(table_data)
        log.print_info("playlists bellow will be crawled")
        print(table.table)

        for pl_obj in playlists:
            playlist_detail = api.get_playlist_detail(pl_obj['id'])
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
