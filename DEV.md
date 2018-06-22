NXSpider
=================

NXSpider，一个强大的（网易云音乐）mp3,mv爬虫，可以下载和收集mp3,mv信息,同时附带多媒体标签信息。采用python编写，mongo数据库(非必须)，递归算法核心实现

[![Software License](https://img.shields.io/pypi/l/Django.svg)](LICENSE.md)
[![platform](https://img.shields.io/badge/python-2.7-green.svg)]()
[![platform](https://img.shields.io/badge/python-3.5-green.svg)]()

[非IT人员或python苦手请看这里](SIMPLE_USE.md)   [历史版本在这里](VERSION.md)  [开发详情在这里](DEV.md)

## 开发及问题(不关心的可以不看了)

### 注意
- 本项目纯粹是学习开发使用，欢迎大家互相讨论，下载的资料请24小时内删除
- 涉及侵权以及版权问题欢迎讨论和提出

### 协助开发或2次开发建议
1. 希望尽可能(yahoo邮件)跟作者(LipsonChan)联系，以及对项目进行加❤
2. 核心代码为NXSpider/bin以及NXSpider/spider/base_driver.py
3. 主要逻辑为通过api获得对于json数据，采用递归+配置方式，自动下载可下载对象
4. 如果有任何反馈，希望回复到项目的issue,注明版本号，运行环境及描述清楚问题

### windows + python2问题
1. 参数输入(目前只有查询)非中文和latin，可能会出现问题
2. 不推荐配置路径中有非latin字符，及路径最好是英文，没测试过
3. 查询结果输出无法显示非中文和latin数据，如韩文（日文可以）

### 其他问题
- 同歌手同名MP3不会被重复下载

### 开发历程
- 基于spider163项目(不满足且有小bug)，开发mongodb以及可以更多爬取项目
- 增加更多url，MV下载，尝试使用eapi发现很难发现加密规则
- 修改项目结构为下载驱动driver和model双层，配合metaclass进行递归式下载，减少后续增量开发工作
- 为了配合Netease app和桌面软件，修改mp3 mp4 tag信息
- 艰难的使用了eyed3，windows超级麻烦(现成的dll还要配置，还有字符集问题)，发现不支持mp4，非常难过
- 发现mutagen，果断弃坑eyed3
- 发布0.0.1版本，可以通过playlist，ablum，aritst_top_mp3爬取和下载mp3,mv
- 发现mongodb可能有人不喜欢，新增无数据库版本（默认无需使用），通过配置可切换
- 新增通过获取最火playlist进行爬取
- 新增了好多功能，读 [VERSION.md](VERSION.md)
- api全靠`fiddler`和猜，**一把辛酸一把泪**

### 下阶段开发
- 通过用户id，爬取该用户所有的歌单 √
- 通过歌手id，爬取该歌手所有专辑 √
- 通过排行版，爬取最新n个歌单 √
- mongodb 可选？不强制（但对于离线则无法加tag，虽然只是个人用） √
- 通过登录(或非登录)，爬取用户收藏的歌单，mv **不安全(明文账号密码)，而且经常登录api会被限，不开放说明**
