@echo off
if "%~1"=="" goto usage

set "EDITOR=c:\Program Files\Sublime Text 3\subl.exe"
if not exist "content/post/%1" mkdir "content/post/%1"
"../hugo.exe" new "post/%1.md"
"%EDITOR%" "content/post/%1.md"
exit /b 0

:usage
echo "newpost <slug>" >&2
echo "e.g. newpost thief/poor-officer-benny" >&2
exit /b 1
