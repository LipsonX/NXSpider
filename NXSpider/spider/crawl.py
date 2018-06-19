#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/5/10.
# email to LipsonChan@yahoo.com
#
from NXSpider.common import tools, log
from NXSpider.common.tools import RETURE_HTML
from NXSpider.spider.api import get_playlist_detail, headers
from NXSpider.spider.playlist import Playlist


def crawl_playlist_by_id(link, download_type=['mp3', 'mv'],
                         save=True, file_check=True):
    playlist_detail = get_playlist_detail(link)
    with tools.ignored(Exception):
        log.print_info("%s author：%s" % (
            "<" + playlist_detail['name'] + ">",
            playlist_detail['creator']['nickname'],
        ))

    playlist_mo = Playlist()
    playlist_mo.parse_model(playlist_detail,
                            save=save, download_type=download_type,
                            file_check=file_check)
    pass


def crawl_playlist_by_page(page, dtype="全部", download_type=['mp3', 'mv'],
                           save=True, file_check=True):
    play_url = "http://music.163.com/discover/playlist/?order=hot&cat={}&limit=35&offset={}"
    play_url = play_url.format(dtype, page * 35)
    playlist_id = []
    titles = []
    try:
        acmsk = {'class': 'msk'}
        scnb = {'class': 'nb'}
        dcu = {'class': 'u-cover u-cover-1'}
        ucm = {'class': 'm-cvrlst f-cb'}
        data = tools.curl(play_url, headers, type=RETURE_HTML)
        lst = data.find('ul', ucm)
        for play in lst.find_all('div', dcu):
            title = play.find('a', acmsk)['title']
            link = play.find('a', acmsk)['href'].replace("/playlist?id=", "")

            playlist_detail = get_playlist_detail(link)
            with tools.ignored(Exception):
                log.print_info("%s author：%s" % (
                    "<" + playlist_detail['name'] + ">",
                    tools.encode(playlist_detail['creator']['nickname']),
                ))

            playlist_mo = Playlist()
            playlist_mo.parse_model(playlist_detail,
                                    save=save, download_type=download_type,
                                    file_check=file_check)

        return titles
    except Exception as e:
        log.print_err("crawl html error：{} type：{} page：{}".format(e, dtype, page))
        raise


def crawl_by_playlists():
    for i in range(36):
        crawl_playlist_by_page(i + 1)
