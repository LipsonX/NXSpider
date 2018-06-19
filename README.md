NXSpider
=================


#### Thanks for project MusicBox and spider163

NXSpider，一个强大的（某云）mp3,mv爬虫，可以下载和收集mp3,mv信息,同事附带多媒体标签信息。采用python编写，mongo数据库，递归算法核心实现

[![Software License](https://img.shields.io/pypi/l/Django.svg)](LICENSE.md)
[![platform](https://img.shields.io/badge/python-2.7-green.svg)]()
[![platform](https://img.shields.io/badge/python-3.5-green.svg)]()

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

#### 配置, <>内容为值，or为可选
	$nxspider config-mongo -mh <host> -mp <port> -mn <db name>
	$nxspider config-spider -path <you_download_path,default> 
	$nxspider config-spider -mvr <240 or 480 or 720 or 1080>
	$nxspider config-spider -tag <1 or 0>
	$nxspider config-spider -tag163 <1 or 0>

#### 配置说明
1. **config-mongo必须运行爬取前配置!!!**，dbname可不指定，默认为nxspider
2. path 强烈建议爬取前配置，```,``` 为多个下载路径分隔符。default指```~/.nxspider/download_files/```
3. 其他配置可选，请查看 ```nxspider -h```
4. ```-tag 1``` 建议保留 ```-tag163 1``` 根据需求保留

#### 搜索
	$nxspider search -ar <artist> [-offset <offset>] [-limit <limit>]
	$nxspider search -pl <playlist> [-offset <offset>] [-limit <limit>]
	$nxspider search -ur <user> [-offset <offset>] [-limit <limit>]
	$nxspider search -mp3 <song> [-offset <offset>] [-limit <limit>]
	$nxspider search -ab <album> [-offset <offset>] [-limit <limit>]
	$nxspider search -mv <mv> [-offset <offset>] [-limit <limit>]

![img](img/search_ab.png)

### 显示歌手唱片
	$nxspider sw-ar-ab -ar <artist_id> [-offset <offset>] [-limit <limit>]

### 根据唱片id(按逗号隔开)爬取歌曲，下载mp3,mv(参数配置)
	$nxspider spls -pl <playlist_id,id2,id3> [-dw <mv,mp3>]
	$nxspider spls -pl 144236857 -dw mv,mp3

![img](img/spider_spls.png)

### 根据歌手id爬取该歌手top50首，
    $nxspider sab -ab <album_id,id1,id2> [-dw <mv,mp3>]
    $nxspider sab -ab 3084625 -dw mv,mp3

![img](img/sar-top-mp3.png)

### 小tips
- 配置 ```-tag163 1``` 直接把下载目录添加到PC版某云软件的下载目录下，软件会自动识别已下载
- 关闭爬取，目前代码是幂等运行，暂时建议直接 ```ctrl + c``` 强制关闭即可


### 已测试的系统兼容列表
<table>
	<tr> <td>win7(GBK) + python2</td> <td>字符集问题</td> </tr>
	<tr> <td>win7(GBK) + python3</td> <td>通过</td> </tr>
	<tr> <td>centos7.2(utf8) + python2</td> <td>通过</td> </tr>
	<tr> <td>centos7.2(utf8) + python3</td> <td>通过</td> </tr>
</table>

### 效果图示例
- 已下载mv

![img](img/mv_download.png)

- 已下载MP3

![img](img/mp3_download.png)

- 已采集数据

![img](img/mongodb_data.png)

## 开发及问题

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

### 下阶段开发
- 通过用户id，爬取该用户所有的歌单
- 通过歌手id，爬取该歌手所有专辑
- 通过排行版，爬取最新n个歌单
- 通过登录，爬取用户收藏的歌单，mv
- mongodb 可选？不强制（但对于离线则无法加tag，虽然只是个人用）
