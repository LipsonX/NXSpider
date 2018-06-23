NXSpider
=================


#### Thanks for project MusicBox and spider163

NXSpider, A powerful for mp3,mv spider, can help you download mp3 and mv with media tags. Base on python, mongodb, and recursion algorithm

[![Software License](https://img.shields.io/pypi/l/Django.svg)](LICENSE.md)
[![platform](https://img.shields.io/badge/python-2.7-green.svg)]()
[![platform](https://img.shields.io/badge/python-3.5-green.svg)]()

## Update History

#### 2018-06-23 v0.0.4
- 增加功能，通过登录爬取用户收藏mv
- 增加功能，通过登录爬取用户所有歌单（包括收藏）
- 增加功能，通过歌单分类，爬取最火歌单
- 增加功能，打印歌单分类
- 增加功能，爬取最火mv
- 优化代码，优化所有文档，优化输出
- 解决小bug：mv id存在但获取不到详情时的代码异常
- 默认mongo非使用，且不安装python依赖包，通过 `pip+req.txt` 进行安装
- 方便windows用户增加小部分bat
- 项目功能已满足作者使用，暂时没什么开发欲望了

#### 2018-06-21 v0.0.3
- 增加功能，通过用户id获得歌单，并爬取歌单信息，mp3,mv
- 增加功能，通过歌手id爬取所有专辑信息，下载所有专辑mp3,mv
- 增加 `VERSION.md`

#### 2018-06-20 v0.0.2
- mongodb改为非必须，默认不需要，并提供相应配置
- 增加功能，爬取特定分类最火歌单信息并下载mp3,mv
- 增加 `SIMPLE_USE.md` 提供最简单的入门说明
- 优化部分代码

#### 2018-06-19 v0.0.1
- 首次发布, mongodb + 递归 + python(3) + tag
- 搜索歌单，歌手，专辑，用户等信息
- 通过歌单，歌手，专辑id，下载mp3, mv
- 所有信息会保存早mongodb中
- 高可配置，所有mp3, mv可以通过配置，增加多媒体标签信息(歌手，专辑，唱片，163comment!!!)