#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/5/24.
# email to LipsonChan@yahoo.com
#
import re
from collections import OrderedDict
from functools import reduce

import requests

from NXSpider.common import log
from NXSpider.spider.common_keys import encrypted_request

base_url = "http://music.163.com"

headers = {
    'Referer': 'http://music.163.com/',
    'Host': 'music.163.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
}

TOP_LIST_ALL = {
    0: ['云音乐新歌榜', '3779629'],
    1: ['云音乐热歌榜', '3778678'],
    2: ['网易原创歌曲榜', '2884035'],
    3: ['云音乐飙升榜', '19723756'],
    4: ['云音乐电音榜', '10520166'],
    5: ['UK排行榜周榜', '180106'],
    6: ['美国Billboard周榜', '60198'],
    7: ['KTV嗨榜', '21845217'],
    8: ['iTunes榜', '11641012'],
    9: ['Hit FM Top榜', '120001'],
    10: ['日本Oricon周榜', '60131'],
    11: ['韩国Melon排行榜周榜', '3733003'],
    12: ['韩国Mnet排行榜周榜', '60255'],
    13: ['韩国Melon原声周榜', '46772709'],
    14: ['中国TOP排行榜(港台榜)', '112504'],
    15: ['中国TOP排行榜(内地榜)', '64016'],
    16: ['香港电台中文歌曲龙虎榜', '10169002'],
    17: ['华语金曲榜', '4395559'],
    18: ['中国嘻哈榜', '1899724'],
    19: ['法国 NRJ EuroHot 30周榜', '27135204'],
    20: ['台湾Hito排行榜', '112463'],
    21: ['Beatport全球电子舞曲榜', '3812895'],
    22: ['云音乐ACG音乐榜', '71385702'],
    23: ['云音乐嘻哈榜', '991319590']
}

PLAYLIST_CLASSES = OrderedDict([
    ('语种', ['华语', '欧美', '日语', '韩语', '粤语', '小语种']),
    ('风格', ['流行', '摇滚', '民谣', '电子', '舞曲', '说唱', '轻音乐', '爵士', '乡村', 'R&B/Soul', '古典', '民族', '英伦', '金属', '朋克', '蓝调', '雷鬼',
            '世界音乐', '拉丁', '另类/独立', 'New Age', '古风', '后摇', 'Bossa Nova']),
    ('场景', ['清晨', '夜晚', '学习', '工作', '午休', '下午茶', '地铁', '驾车', '运动', '旅行', '散步', '酒吧']),
    ('情感', ['怀旧', '清新', '浪漫', '性感', '伤感', '治愈', '放松', '孤独', '感动', '兴奋', '快乐', '安静', '思念']),
    ('主题', ['影视原声', 'ACG', '儿童', '校园', '游戏', '70后', '80后', '90后', '网络歌曲', 'KTV', '经典', '翻唱', '吉他', '钢琴', '器乐', '榜单', '00后'])
])

ALL_CLASSES = reduce(lambda x, y: x + y, [v for k, v in PLAYLIST_CLASSES.items()])

MV_TYPE = ['ALL', 'ZH', 'EA', 'KR', 'JP']


# 搜索单曲(1)，歌手(100)，专辑(10)，歌单(1000)，用户(1002) *(type)*
search_types = {
    'mp3': 1,
    'artist': 100,
    'album': 10,
    'playlist': 1000,
    'user': 1002,
    'mv': 1004,
}


def api_request(url, data=None, method="get", json=True,
                session=None, headers=headers):
    """
    request and try
    :param url:
    :param data:
    :param method:
    :param json:
    :param session:
    :type session:  requests.Session
    :param headers:
    :return:
    """
    url = base_url + url
    request_obj = session or requests

    # update cookies
    if isinstance(request_obj, requests.Session):
        for cookie in request_obj.cookies:
            if cookie.name == '__csrf':
                data['csrf_token'] = cookie.value
                break

    # encrypt
    data = encrypted_request(data)

    method = 'get' if not data and method == 'get' else 'post'
    request_method = getattr(request_obj, method, None) or request_obj.get
    try:
        req = request_method(url, data=data, headers=headers, timeout=10)
        req.encoding = "UTF-8"
        res = req.json() if json else req.text
        # if session:
        #     session.cookies.save()
        return res
    except ValueError as e:
        log.print_err("api do not return a valuable json")
        return {}
    except requests.exceptions.RequestException as e:
        log.print_warn("request error: %s" % url)
        return {}


def get_top_songlist(idx=0, offset=0):
    action = TOP_LIST_ALL[idx][1]
    res = api_request(action, json=False)
    if not res:
        return None

    songids = re.findall(r'/song\?id=(\d+)', res)
    if not songids:
        return None

    songids = list(set(songids))
    details = get_mp3_details(songids, offset=offset)
    return details


def get_mp3_link(song_id):
    # obj = '{"ids":[' + str(song_id) + '], br:"320000",csrf_token:"csrf"}'
    data = {'ids': [song_id], 'br': 320000, 'csrf_token': 'csrf'}
    url = "/weapi/song/enhance/player/url"
    res = api_request(url, data)
    if res and res['code'] == 200:
        return res['data'][0]['url']


def get_mp3_links(song_ids):
    # obj = '{"ids":[' + str(song_id) + '], br:"320000",csrf_token:"csrf"}'
    data = {'ids': song_ids, 'br': 320000, 'csrf_token': 'csrf'}
    url = "/weapi/song/enhance/player/url"
    res = api_request(url, data)
    if res and res['code'] == 200:
        return {x['id']: x['url'] for x in res['data']}


def get_mp3_details(song_ids, offset=0):
    tmpids = song_ids[offset:]
    tmpids = tmpids[0:100]
    tmpids = list(map(str, tmpids))
    action = '/api/song/detail?ids=[{}]'.format(  # NOQA
        ','.join(tmpids))

    res = api_request(action)
    if res and res['code'] == 200:
        return {x['id']: x for x in res['songs']}


def get_mv_link(mv_id, r):
    data = {'id': mv_id, 'r': r, 'csrf_token': 'csrf'}
    url = "/weapi/song/enhance/download/mv/url"

    res = api_request(url, data)
    if res and res['code'] == 200:
        return res['data']['url']


def get_mv_detail(mv_id):
    data = {'id': mv_id, 'csrf_token': 'csrf'}
    url = "/weapi/v1/mv/detail"

    res = api_request(url, data)
    return res.get('data', None)


def get_playlist_detail(playlist_id):
    url = "/api/playlist/detail?id={}&upd" \
        .format(playlist_id)

    res = api_request(url)
    return res.get('result', None)


def get_playlist_detail_v3(id):
    action = '/weapi/v3/playlist/detail'
    data = {'id': id, 'total': 'true', 'csrf_token': 'csrf', 'limit': 1000, 'n': 1000, 'offset': 0}

    res = api_request(action, data)
    return res.get('playlist', None)


def get_top_playlists(category='全部', order='hot', offset=0, limit=50):
    """
    get playlists, but not detail
    :param category:
    :param order:
    :param offset:
    :param limit:
    :return:
    """
    action = u'/api/playlist/list?cat={}&order={}&offset={}&total={}&limit={}'.format(  # NOQA
        category, order, offset, 'true' if offset else 'false',
        limit)  # NOQA

    res = api_request(action)
    return res.get('playlists', None)


# may be not useful
def get_playlist_classes():
    action = '/weapi/playlist/catalogue'
    res = api_request(action, json=False)
    if res and res['code'] == 200:
        return re


def get_playlist_catelogs():
    path = '/weapi/playlist/catalogue'
    return api_request(path, json=False)


def top_artists(offset=0, limit=100):
    action = '/api/artist/top?offset={}&total=false&limit={}'.format(  # NOQA
        offset, limit)
    res = api_request(action)
    return res.get('artists', None)


def get_artists_songs(artist_id):
    action = '/api/artist/{}'.format(artist_id)
    res = api_request(action)
    if res and res['code'] == 200:
        return res


def get_artist_album(artist_id, offset=0, limit=50):
    action = '/api/artist/albums/{}?offset={}&limit={}'.format(
        artist_id, offset, limit)
    res = api_request(action)
    if res and res['code'] == 200:
        return res
    # if res and res['code'] == 200:
    #     return res['hotAlbums']
    # return res.get('hotAlbums', None)


def get_album_detail(album_id):
    action = '/api/album/{}'.format(album_id)
    res = api_request(action)
    return res.get('album', None)


def search(s, stype=1, offset=0, total='true', limit=60):
    if isinstance(stype, str):
        if stype in search_types:
            stype = search_types[stype]
        else:
            return None

    action = '/api/search/get'
    data = {
        's': s,
        'type': stype,
        'offset': offset,
        'total': total,
        'limit': limit
    }
    res = api_request(action, data)
    return res.get('result', None)


# has been change, fuck!
def user_playlist(uid, session=None, offset=0, limit=50):
    action = '/weapi/user/playlist'
    data = {'uid': uid, 'csrf_token': 'csrf',
            'limit': limit, 'offset': offset,
            'wordwrap': 7}

    res = api_request(action, data=data, session=session)
    return res.get('playlist', None)


def user_playlist_old(uid, offset=0, limit=100, session=None):
    action = '/api/user/playlist/?offset={}&limit={}&uid={}'.format(  # NOQA
        offset, limit, uid)

    res = api_request(action, session=session)
    return res.get('playlist', None)


def my_subcount(session):
    action = '/weapi/subcount'
    res = api_request(action, data={}, session=session)

    return res


def my_mvs(session):
    action = '/weapi/mv/sublist'
    data = dict(
        offset=0,
        limit=1000,
    )
    res = api_request(action, data=data, session=session)

    return res.get('data', [])


def hot_mvs():
    # todo, wait to find out how to encrypt and decrypt
    action = '/api/mv/toplist'
    action = '/api/mv/first'
    action = '/api/mv/hot'  # well done

    data = dict(
        cat=u'内地',
        order='hot',
        offset=0,
        limit=50,
    )

    res = api_request(action, data=data)
    return res


def top_mvs(offset=0, limit=50, type='ALL'):
    # todo, wait to find out how to encrypt and decrypt
    action = '/api/mv/toplist'  # o, l
    action = '/api/mv/first'
    action = '/api/mv/all'  # well done, o, l

    action = '/weapi/mv/all'

    data = dict(
        area='kr',
        # type='JP',
        # total='true',
        # order='hot',
        offset=0,
        limit=20,
    )

    res = api_request(action, data=data)
    return res


def all_mvs(offset=0, limit=50):
    action = '/weapi/mv/all'
    data = dict(
        offset=offset,
        limit=limit,
    )
    res = api_request(action, data=data)
    return res


def phone_login(username, password, session):
    """

    :param username:
    :param password: must be encrypt by md5 hex
    :param session:
    :type session: requests.Session
    :return:
    """
    action = '/weapi/login/cellphone'
    data = {
        'phone': username,
        'password': password,
        'rememberLogin': 'true'
    }

    res = api_request(action, data=data, session=session)
    if res:
        return res


def login(username, password, session):
    """
    :type username: str
    :param username:
    :param password: must be encrypt by md5 hex
    :param session:
    :type session: requests.Session
    :return:
    """
    if username.isdigit():
        return phone_login(username, password, session)
    action = '/weapi/login'
    client_token = '1_jVUMqWEPke0/1/Vu56xCmJpo5vP1grjn_SOVVDzOc78w8OKLVZ2JH7IfkjSXqgfmh'
    session.cookies.load()
    data = {
        'username': username,
        'password': password,
        'rememberLogin': 'true',
        'clientToken': client_token,
    }
    res = api_request(action, data=data, session=session)
    if res:
        return res
