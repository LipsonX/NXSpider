NXSpider
=================


#### Thanks for project MusicBox and spider163

NXSpider, A powerful for mp3,mv spider, can help you download mp3 and mv with media tags. Base on python, mongodb, and recursion algorithm

[![Software License](https://img.shields.io/pypi/l/Django.svg)](LICENSE.md)
[![platform](https://img.shields.io/badge/python-2.7-green.svg)]()
[![platform](https://img.shields.io/badge/python-3.5-green.svg)]()

## Update History

#### 2018-06-21 v0.0.3
- 增加通过用户id获得歌单，并爬取歌单信息，mp3,mv
- 增加通过歌手id爬取所有专辑信息，下载所有专辑mp3,mv
- 增加 `VERSION.md`

#### 2018-06-20 v0.0.2
- mongodb改为非必须，默认不需要，并提供相应配置
- 增加爬取特定分类最火歌单信息并下载mp3,mv
- 增加 `SIMPLE_USE.md` 提供最简单的入门说明
- 优化部分代码

#### 2018-06-19 v0.0.1
- 首次发布, mongodb + 递归 + python(3) + tag
- 搜索歌单，歌手，专辑，用户等信息
- 通过歌单，歌手，专辑id，下载mp3, mv
- 所有信息会保存早mongodb中
- 高可配置，所有mp3, mv可以通过配置，增加多媒体标签信息(歌手，专辑，唱片，163comment!!!)