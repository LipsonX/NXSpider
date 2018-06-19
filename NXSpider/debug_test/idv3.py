#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/5/16.
# email to LipsonChan@yahoo.com
#
import locale

import eyed3
from mutagen.mp4 import MP4

from NXSpider.utility.idv3_base import delete_163comment
from NXSpider.utility.modify_idv3 import attach_media_tag_by_path, attach_media_tag_by_conf_path

from mutagen.id3 import ID3, TALB, COMM
from mutagen.easyid3 import EasyID3
TALB
COMM
MP4
# ['TIT2', 'TPE1', 'TRCK', 'TALB', 'TPOS', 'TSSE', 'APIC:', 'COMM::XXX']
#  名称      歌手  trackNum   专辑     pos     编码              comments
# 'TPE2' 'aART' album_artist

attach_media_tag_by_path(u'E:\\test')
attach_media_tag_by_conf_path()

# a = ID3(u'E:\\薛之谦 - 丑八怪.mp3', v2_version=3)
#
# a = MP4(u'E:\\(G)I-DLE - LATATA.mp4')
#
# a = eyed3.load(u'E:\\薛之谦 - 丑八怪.mp3')
# a.tag.comments.remove('')
# a = eyed3.load(u'E:\\(G)I-DLE - LATATA.mp3')
# a = eyed3.load(u'E:\\(G)I-DLE - LATATA.mp4')
# a.tag.title("test")
# a.tag.comments.remove('')

locale.getlocale(locale.LC_ALL)
file = u"E:/新建文件夹/Billion - Dancing Alone_wapi - 副本.mp3"
file = u"D:\\Project\\python\\music.crawl\\download_files\\mp3\\1호선 뮤직\\1호선 뮤직 - 열대야.mp3"
file = u"D:\\Project\\python\\music.crawl\\download_files\\mp3\\Dal★shabet\\Dal★shabet - JOKER.mp3"
delete_163comment(file)
print('a')

attach_media_tag_by_conf_path()

print('a')
