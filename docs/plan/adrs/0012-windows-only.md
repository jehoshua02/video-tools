# 0012. Target Windows only

## Status
Accepted

## Context
The tool runs on the author's own Windows machine ([[0003-local-cli-distribution]]).

## Decision
Support and test on Windows only. `ffmpeg` and `ffprobe` must be on PATH.

## Consequences
- No macOS/Linux testing or guarantees.
- File names are compared case-insensitively (`.MP4` = `.mp4`), matching NTFS.
- Can still use pathlib; porting later is possible but not planned.
