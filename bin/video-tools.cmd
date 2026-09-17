@echo off
rem Kept on one line: cmd re-reads this file after each line, and `video-tools update` may rewrite it mid-run.
rem python must be the last command so its exit code becomes this script's exit code.
rem -P keeps the current folder off the import path, so a video_tools folder there can't shadow this install.
setlocal & set "PYTHONPATH=%~dp0.." & python -P -m video_tools %*
