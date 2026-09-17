@echo off
rem Kept on one line: cmd re-reads this file after each line, and `video-tools update` may rewrite it mid-run.
rem python must be the last command so its exit code becomes this script's exit code.
setlocal & set "PYTHONPATH=%~dp0.." & python -m video_tools %*
