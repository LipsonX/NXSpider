#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/5/11.
# email to LipsonChan@yahoo.com
#
import hashlib

import requests

from NXSpider.common import tools, log
from NXSpider.common.constant import all_download_type
from NXSpider.spider.api import get_playlist_detail, get_mp3_links, get_album_detail, get_top_playlists, \
    get_playlist_classes, \
    top_artists, get_artists_songs, get_artist_album, get_mp3_details, search, phone_login, login, user_playlist, \
    get_playlist_detail_v3, get_playlist_catelogs, hot_mvs, all_mvs, top_mvs
from NXSpider.spider.playlist import Playlist

# def playlist_by_id(link, download_type=all_download_type,
#                    save=True, file_check=True):
#     playlist_detail = get_playlist_detail(link)
#     with tools.ignored(Exception):
#         log.print_info("%s author：%s" % (
#             "<" + playlist_detail['name'] + ">",
#             playlist_detail['creator']['nickname'],
#         ))
#
#     playlist_mo = Playlist()
#     playlist_mo.parse_model(playlist_detail,
#                             save=save, download_type=download_type,
#                             file_check=file_check)
#     pass


# def playlist_by_page(page, type=u"全部"):
#     play_url = constant.play_url.format(type, page * 35)
#     titles = []
#     try:
#         log.print_info("begin crawl playlist page: {}, type: {}".format(page, type))
#         acmsk = {'class': 'msk'}
#         scnb = {'class': 'nb'}
#         dcu = {'class': 'u-cover u-cover-1'}
#         ucm = {'class': 'm-cvrlst f-cb'}
#         data = tools.curl(play_url, constant.header, type=constant.RETURE_HTML)
#         lst = data.find('ul', ucm)
#         for play in lst.find_all('div', dcu):
#             title = tools.encode(play.find('a', acmsk)['title'])
#             link = tools.encode(play.find('a', acmsk)['href']).replace("/playlist?id=", "")
#             # playlist_by_id(link)
#             print("link: {}, title: {}".format(link, title))
#     except Exception as e:
#         log.print_err("playlist page error：{} type：{} page：{}".format(e, type, page))
#         log.print_err(e)


# def playlist_all_page():
#     cf = "全部"
#     for i in range(36):
#         playlist_by_page(i + 1, cf)

# test = get_mv_details([5322493,239037])
test = top_mvs()
test = all_mvs()
test = hot_mvs()
test = get_playlist_catelogs()
test = get_playlist_classes()
test = get_top_playlists()
test = user_playlist(48872048)
test = get_playlist_detail(92024088)
test = get_playlist_detail(2246057871)
test = get_playlist_detail(107020750)
test = get_playlist_detail_v3(107020750)

p = hashlib.md5('000'.encode('utf-8')).hexdigest()
s = requests.Session()

test = user_playlist(92024088, session=s)
test = get_playlist_detail(107020750)


test = search('周杰伦', stype=100)
test = top_artists()
test = get_playlist_classes()
test = get_mp3_details([412902496,412902496,412902496])

test = get_artists_songs(9621)
test = get_artist_album(9621)


test = top_artists()
# test = playlist_classes()
test = get_top_playlists()

test = get_album_detail(32324)

# test = get_mp3_link(412902496)
# playlist_by_id(466225104)
tests = get_mp3_links([412902496, 326904])
# http://music.163.com/api/song/detail?ids=[412902496,326904] work
# http://music.163.com/api/album/32324 don't work
# http://music.163.com/#/artist?id=9621
# http://music.163.com/api/artist/9621  don't work
# playlist_all_page()




print('a')
