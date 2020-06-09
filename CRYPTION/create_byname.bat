@echo off

if [%1]==[] goto usage

Archiver.exe config.json %1

@echo done!
goto :eof

:usage
@echo Usage: %0 ^<folder_name^>
PAUSE
exit /B 1