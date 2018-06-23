@ECHO OFF

goto start

# created by Lipson on 2018/6/5.
# email to LipsonChan@yahoo.com
#
# this script will set current path as a pythonpath, and run python
# usage :

:start
setlocal

echo "you need replace ',' by ':' in this bat"

:: get all params
:param
set str=%1
if "%str%"=="" (
    goto end
)

set "str=%str::=,%"
set allparam=%allparam% %str%
shift /0
goto param

:end


::run
set PYTHONPATH=%cd%
python3 %allparam%
endlocal