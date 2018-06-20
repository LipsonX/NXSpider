#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/5/17.
# email to LipsonChan@yahoo.com
#
import os
from functools import reduce

from mutagen import id3
from mutagen.id3 import ID3
from mutagen.mp4 import MP4

from NXSpider.common.config import Config
from NXSpider.common.encrypt import aes_ecb
from NXSpider.model.export import Mp3Model, Mp4Model

key_names = ['title', 'artist', 'album', 'album_artist', 'track_num', 'comment']
encoding_keys = ['title', 'artist', 'album', 'album_artist', 'comment']
mutagen_idv3_key_map = {
    'title': 'TIT2',
    'artist': 'TPE1',
    'album': 'TALB',
    'album_artist': 'TPE2',
    'track_num': 'TRCK',
    'comment': 'COMM'
}

mugagen_mp4_key_map = {
    'title': '\xa9nam',
    'artist': '\xa9ART',
    'comment': '\xa9cmt',
}
aes_code = "#14ljk_!\]&0U<'("


# @tools.ignored(Exception)
def attach_mp3_idv3(doc, file):
    """
    :type doc: Mp3Model
    :param doc:
    :param file:
    :return:
    """
    artists = [('["%s",%d]' % (x['name'], x.id)) for x in doc.artists]
    artists_str = reduce(lambda x, y: x + "," + y, artists)

    authors = reduce(lambda x, y: x + ',' + y, [x['name'] for x in doc.artists])
    data = {
        'title': doc['name'],
        'artist': authors,
        'album': doc['album']['name'],
        'album_artist': authors,
        'track_num': str(doc['no']),
    }

    if Config().get_media_tag_163():
        comment_plaintext = u'music:{"musicId":%d,"musicName":"%s","bitrate":320000,' \
                            u'"albumId":%d,"album":"%s", "artist":[%s]}' \
                            % (doc.id, doc['name'], doc.album.id, doc.album['name'],
                               artists_str)
        comment = "163 key(Don't modify):" + aes_ecb(comment_plaintext, aes_code).decode()
        data['comment'] = comment

    try:
        mp3 = ID3(file, v2_version=3)
        for k, v in data.items():
            if k not in mutagen_idv3_key_map:
                continue

            if k == 'comment':
                mp3.add(id3.COMM(lang='XXX', text=v))
                continue

            attr_type = getattr(id3, mutagen_idv3_key_map[k], None)
            if attr_type:
                mp3.add(attr_type(text=v))

        mp3.save(v2_version=3)
    except Exception as e:
        return False
    return True


# @tools.ignored(Exception)
def attach_mp4_tag(doc, file):
    """
    :type doc: Mp4Model
    :param doc:
    :param file:
    :return:
    """
    authors = reduce(lambda x, y: x + u',' + y, [x['name'] for x in doc.artists])
    data = {
        'title': doc['name'],
        'artist': authors,
    }

    if Config().get_media_tag_163():
        comment_plaintext = u'mv:{"title":"%s","mvId":%d,"artistId":%d,' \
                            u'"artistName":"%s","pubTime":"%s","bitrate":%d}' \
                            % (doc['name'], doc.id, doc.artists[0].id,
                               doc.artists[0]['name'], doc['publishTime'],
                               doc['download_video_r'])
        comment = "163 key(Don't modify):" + aes_ecb(comment_plaintext, aes_code).decode()
        data['comment'] = comment

    try:
        mp4 = MP4(file)
        for k, v in data.items():
            if k not in mugagen_mp4_key_map:
                continue
            mp4[mugagen_mp4_key_map[k]] = v

        mp4.save()
    except Exception as e:
        return False
    return True


def attach_media_tag(doc, file):
    """
    attach a media idv3
    :param doc:
    :param file:
    :return:
    """
    if not os.path.exists(file):
        return False

    if isinstance(doc, Mp3Model):
        return attach_mp3_idv3(doc, file)
    elif isinstance(doc, Mp4Model):
        return attach_mp4_tag(doc, file)
