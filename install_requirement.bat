@ECHO OFF

goto start

# created by Lipson on 2018/12/15.
# email to LipsonChan@yahoo.com
#
# this script will set current path as a pythonpath, and run python
# usage :

:start

pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r requirements.txt
pause