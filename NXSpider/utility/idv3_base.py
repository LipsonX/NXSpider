#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/5/16.
# email to LipsonChan@yahoo.com
#
import os

import eyed3
from eyed3.id3 import ID3_V2_3
from mutagen.id3 import ID3, Encoding
from mutagen.mp4 import MP4
from mutagen import id3

key_names = ['title', 'artist', 'album', 'album_artist', 'track_num', 'comment']
encoding_keys = ['title', 'artist', 'album', 'album_artist', 'comment']
# ['TIT2', 'TPE1', 'TRCK', 'TALB', 'TPOS', 'TSSE', 'APIC:', 'COMM::XXX']
#  名称      歌手  trackNum   专辑     pos     编码              comments
# 'TPE2' 'aART' album_artist
mutagen_idv3_key_map = {
    'title': 'TIT2',
    'artist': 'TPE1',
    'album': 'TALB',
    'album_artist': 'TPE2',
    'track_num': 'TRCK',
    'commemt': 'COMM'
}

mugagen_mp4_key_map = {
    'title': '\xa9nam',
    'artist': '\xa9ART',
    'comment': '\xa9cmt',
}


def delete_163comment(file):
    """
    :type file: str
    :param file:
    :return:
    """
    if not os.path.exists(file):
        return
    suffix = file[file.rfind('.'):]
    if suffix not in ['.mp3', '.mp4']:
        return

    try:
        id3_file = eyed3.load(file)
        id3_file.initTag(version=ID3_V2_3)
        id3_file.tag.comments.remove('', lang=b'XXX')
        id3_file.tag.save()
    except Exception as e:
        raise e


def attach_mp3_idv3(filename, data):


    try:
        mp3 = ID3(filename, v2_version=3)
        for k, v in data.items():
            if k not in mutagen_idv3_key_map:
                continue

            if k == 'comment':
                mp3.add(id3.COMM(lang='XXX', text=v))
                continue

            attr_type = getattr(id3, mutagen_idv3_key_map[k], None)
            if attr_type:
                mp3.add(attr_type(text=v))

        mp3.save()
    except Exception as e:
        return False
    return True


def attach_mp4_tag(filename, data):
    if not os.path.exists(filename):
        return False

    try:
        mp4 = MP4(filename)
        for k, v in data.items:
            if k not in mugagen_mp4_key_map:
                continue
            mp4[mugagen_mp4_key_map[k]] = v

        mp4.save()
    except Exception as e:
        return False
    return True


def attach_media_idv3(filename, data, encoding_func=None):
    """
    attach data to idv3 of a file
    :param encoding_func: change encoding of values
    :type encoding_func: function | None
    :type filename: str
    :param filename:
    :type data: dict
    :param data:
    :return:
    """
    if not os.path.exists(filename):
        return
    suffix = filename[filename.rfind('.'):]
    if suffix not in ['.mp3', '.mp4']:
        return

    try:
        id3_file = eyed3.load(filename)
        id3_file.initTag(version=ID3_V2_3)

        for k, v in data.items():
            if k not in key_names:
                continue

            if encoding_func and k in encoding_keys:
                v = encoding_func(v)

            if k == 'comment':
                id3_file.tag.comments.set(v, description=u'', lang=b'XXX')
                continue

            setattr(id3_file.tag, k, v)
        id3_file.tag.save()
    except Exception as e:
        return False

    return True
