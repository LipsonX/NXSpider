NXSpider
=================

NXSpider，一个强大的（网易云音乐）mp3,mv爬虫，可以下载和收集mp3,mv信息,同时附带多媒体标签信息。采用python编写，mongo数据库(非必须)，递归算法核心实现

[![Software License](https://img.shields.io/pypi/l/Django.svg)](LICENSE.md)
[![platform](https://img.shields.io/badge/python-2.7-green.svg)]()
[![platform](https://img.shields.io/badge/python-3.5-green.svg)]()

[非IT人员或python苦手请看这里](SIMPLE_USE.md)   [历史版本在这里](VERSION.md)  [开发详情在这里](DEV.md)

## 灵感来自

[chengyumeng/spider163](https://github.com/chengyumeng/spider163)

[Binaryify/NeteaseCloudMusicApi](https://github.com/Binaryify/NeteaseCloudMusicApi)

[darknessomi/musicbox](https://github.com/darknessomi/musicbox)

[sqaiyan/netmusic-node](https://github.com/sqaiyan/netmusic-node)

## 功能特性
1. 采用命令行形式运行，配置在个人账号目录下```~/.nxspider/```
2. 搜索歌单，歌手，专辑，用户等信息
3. 通过各种方法，如歌单，歌手，专辑等，下载mp3, mv
4. 所有信息会保存早mongodb中
5. 所有mp3, mv可以通过配置，增加多媒体标签信息(歌手，专辑，唱片，163comment!!!)

## 运行
### 运行依赖
1. python3(推荐) or python2, 请配置好path
2. windows or linux
3. [mongodb](https://docs.mongodb.com/manual/installation/)

### Git clone安装
    $ git clone https://github.com/Grass-CLP/NXSpider.git && cd NXSpider
    $ python(3) setup.py install

### pip安装
待补充

### 卸载
    $ pip(3) uninstall nxspider
    $ rm -rf ~/.nxspider

### 运行预说明
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

### 使用指南
#### 简单示例
	$nxspider -h
	$nxspider -v
	$nxspider config-check

#### 配置, <>内容为值，or为可选
	$nxspider config-mongo -mh <host> -mp <port> -mn <db name>
	$nxspider config-mongo -nomongo <1 or 0>
	$nxspider config-spider -path <you_download_path,default> 
	$nxspider config-spider -mvr <240 or 480 or 720 or 1080>
	$nxspider config-spider -tag <1 or 0>
	$nxspider config-spider -tag163 <1 or 0>
	$nxspider config-check

#### 配置说明
1. ~~config-mongo必须运行爬取前配置!!!，dbname可不指定，默认为nxspider~~
2. 默认无mongodb模式，需要采集数据则通过配置第一条即可 `nxspider config-mongo ..`
3. 一旦配置了 `mongodb -mh` 则 `-nomogo` 会自动设置为0，即配置了host就会使用的意思
2. path **强烈建议**爬取前配置，```,``` 为多个下载路径分隔符。default指`~/.nxspider/download_files/`
3. 其他配置可选，请查看 `nxspider -h`
4. ```-tag 1``` 建议保留 `-tag163 1` 根据需求保留
6. 配置完建议执行 ```nxspider config-check``` 检查配置正确性

#### 搜索
	$nxspider search -ar <artist> [-offset <offset>] [-limit <limit>]
	$nxspider search -pl <playlist> [-offset <offset>] [-limit <limit>]
	$nxspider search -ur <user> [-offset <offset>] [-limit <limit>]
	$nxspider search -mp3 <song> [-offset <offset>] [-limit <limit>]
	$nxspider search -ab <album> [-offset <offset>] [-limit <limit>]
	$nxspider search -mv <mv> [-offset <offset>] [-limit <limit>]

![img](img/search_ab.png)

#### 显示歌手唱片
	$nxspider sw-ar-ab -ar <artist_id> [-offset <offset>] [-limit <limit>]

#### 根据唱片id(按逗号隔开)爬取歌曲，下载mp3,mv(参数配置)
	$nxspider spls -pl <playlist_id,id2,id3> [-dw <mv,mp3>]
	$nxspider spls -pl 144236857 -dw mv,mp3

![img](img/spider_spls.png)

#### 根据歌手id爬取该歌手top50首，
    $nxspider sab -ab <album_id,id1,id2> [-dw <mv,mp3>]
    $nxspider sab -ab 3084625 -dw mv,mp3

![img](img/sar-top-mp3.png)

#### 小tips
- 配置 ```-tag163 1``` 直接把下载目录添加到PC版某云软件的下载目录下，软件会自动识别已下载
- 关闭爬取，目前代码是幂等运行，暂时建议直接 ```ctrl + c``` 强制关闭即可


#### 系统兼容
| 系统及平台  |   结果     |
|   ---     |    ---    |
| win7(GBK) + python2 | 字符集问题 |
| win7(GBK) + python3 | 通过 |
| win10(GBK) + python2 | 字符集问题 |
| win10(GBK) + python3 | 通过 |
| centos7.2(utf8) + python2 | 通过 |
| centos7.2(utf8) + python3 | 通过 |
| mac + python | 待补充 |
</table>

#### 效果图示例
- 已下载mv

![img](img/mv_download.png)

- 已下载MP3

![img](img/mp3_download.png)

- 已采集数据

![img](img/mongodb_data.png)
