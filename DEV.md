NXSpider
=================

NXSpider， NetEase X Spider，一个强大的（网易云音乐）mp3,mv爬虫，可以下载和收集mp3,mv信息,同时附带多媒体标签信息。采用python编写，mongo数据库(非必须)，递归算法核心实现

[![Software License](https://img.shields.io/pypi/l/Django.svg)](LICENSE.md)
![platform](https://img.shields.io/badge/python-2.7-green.svg)
![platform](https://img.shields.io/badge/python-3.5-green.svg)

[新手先看这里](SIMPLE_USE.md) | [历史版本在这里](VERSION.md) | [开发详情在这里](DEV.md)

## 开发及问题(不关心的可以不看了)

### 开发调试
1. 已安装则采用(下文采用该方式进行说明)：
```
$nxspider ...
```
2. 未安装+win采用(未安装指没执行setup.py,只用代码运行)：
```
bash_python(3) NXSipder/bin/cli.py ...
```
3. 未安装+linux采用：
```
PYTHONPATH=. python(3) NXSipder/bin/cli.py ...
```
4. 注意,win下采用bash_python时，分割符 ```,``` 必须改为 ```:``` eg.
```
$bash_python.bat NXSpider/bin/cli.py config-spider -path d:\netease_dw:default
```

### 配置说明
1. ~~config-mongo必须运行爬取前配置!!!，dbname可不指定，默认为nxspider~~
2. 默认无mongodb模式，需要采集数据则通过配置第一条即可 `nxspider config-mongo ..`
3. 一旦配置了 `mongodb -mh` 则 `-nomogo` 会自动设置为0，即配置了host就会使用的意思
2. path **强烈建议**爬取前配置，```,``` 为多个下载路径分隔符。default指`~/.nxspider/download_files/`
3. 其他配置可选，请查看 `nxspider -h`
4. ```-tag 1``` 建议保留 `-tag163 1` 根据需求保留
6. 配置完建议执行 ```nxspider config-check``` 检查配置正确性

### 注意
- 本项目纯粹是学习开发使用，欢迎大家互相讨论，下载的资料请24小时内删除
- 涉及侵权以及版权问题欢迎讨论和提出

### 协助开发或2次开发建议
1. 希望尽可能(yahoo邮件)跟作者(LipsonChan)联系，以及对项目进行加★
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
