#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/6/23.
# email to LipsonChan@yahoo.com
#
from terminaltables import AsciiTable


def print_playlist(pls):
    table = AsciiTable([["ID", "Name", "User", "PlayCount"]])
    table_data = [[str(item['id']), item['name'],
                   item['creator']['nickname'],
                   str(item['playCount']),
                   ] for item in pls]
    table.table_data.extend(table_data)
    print(table.table)
    pass


def print_albums(abs):
    from terminaltables import AsciiTable
    table = AsciiTable([["ID", "Album", "Artist", "ArtistID"]])
    table_data = [[str(item['id']), item['name'],
                   ','.join([ar['name'] for ar in item['artists']]),
                   ','.join([str(ar['id']) for ar in item['artists']]),
                   ] for item in abs]
    table.table_data.extend(table_data)
    print(table.table)
    pass


def print_mp3s(mp3s):
    table = AsciiTable([["ID", "Name", "Album", "AlbumID", "Artist", "ArtistID"]])
    table_data = [[str(item['id']), item['name'],
                   item['album']['name'], item['album']['id'],
                   ','.join([ar['name'] for ar in item['artists']]),
                   ','.join([str(ar['id']) for ar in item['artists']]),
                   ] for item in mp3s]
    table.table_data.extend(table_data)
    print(table.table)
    pass


def print_users(users):
    table = AsciiTable([["ID", "Name", "Signature"]])
    table_data = [[str(item['userId']), item['nickname'],
                   item['signature'],
                   ] for item in users]
    table.table_data.extend(table_data)
    print(table.table)
    pass


def print_artists(artists):
    table = AsciiTable([["ID", "Name", "AlbumNum", "MVNum"]])
    table_data = [[str(item['id']), item['name'],
                   str(item['albumSize']),
                   str(item['mvSize'])
                   ] for item in artists]
    table.table_data.extend(table_data)
    print(table.table)
    pass


def print_mvs(mvs):
    table = AsciiTable([["ID", "Name", "Artist", "ArtistID", "Duration", "PlayCount"]])
    table_data = [[str(item['id']), item['name'],
                   item['artistName'],
                   item['artistId'],
                   '%02d:%02d' % divmod(int(item['duration'] / 1000), 60),
                   item['playCount'],
                   ] for item in mvs]
    table.table_data.extend(table_data)
    print(table.table)
    pass
