#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/6/19.
# email to LipsonChan@yahoo.com
#
from NXSpider.spider.album import Album
from NXSpider.spider.artist import Artist
from NXSpider.spider.mp3 import Mp3
from NXSpider.spider.mv import MV
from NXSpider.spider.playlist import Playlist
from NXSpider.spider.user import User

no_rec_artist_mo = Artist(
    __parse_recursion__={}
)

no_rec_album_mo = Album(
    __model_rfilter__={'artist', 'songs'},
    __parse_recursion__={'artists': no_rec_artist_mo}
)

no_rec_mv_mo = MV(
    __parse_recursion__={'artists': no_rec_artist_mo}
)

dw_mp3_mo = Mp3(
    __parse_recursion__={
        'artists': no_rec_artist_mo,
        'album': no_rec_album_mo,
        'mv': no_rec_mv_mo,
    }
)

playlist_mo = Playlist(
    __model_rfilter__={'artist'},
    __parse_recursion__={
        'mp3': dw_mp3_mo,
        'creator': User(),
    }
)

artist_mo = Artist(
    __model_rfilter__={'artist'},
    __parse_recursion__={
        'mp3': dw_mp3_mo,
    }
)

album_mo = Album(
    __model_rfilter__={'artist'},
    __parse_recursion__={
        'mp3': dw_mp3_mo,
        'artists': no_rec_artist_mo,
    }
)

artist_album_mo = Artist(
    __model_rfilter__={},
    __parse_recursion__={
        'albums': album_mo,
        'artists': no_rec_artist_mo,
    }
)
