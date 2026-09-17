# 0010. Failure handling, temp files, per-video error logs

## Status
Accepted

## Context
A crash mid-encode must not leave a partial `.mp4`, since [[0006-keep-originals]]
would then skip that video forever. Temp files must not be left behind either.
Errors need to be easy to find next to the video they belong to.

## Decision
- Encode to `<stem>.mp4.partial` (ffmpeg `-f mp4`), rename to `<stem>.mp4` only on success.
- On failure, delete the `.partial` file.
- At the start of each run, delete any leftover `*.mp4.partial` in the folder (from a killed run).
- On failure, write ffmpeg/ffprobe stderr and the command to `<stem>.error.log`, next to the original.
- On success, delete any stale `<stem>.error.log`.
- Keep going after errors; exit non-zero if any file failed.
- Failed files are retried on the next run (no `.mp4` exists yet).
- The script's own artifacts (`.partial`, `.error.log`) are skipped without probing.

## Consequences
- Sort order groups `foo.error.log`, `foo.mkv`, `foo.mp4`.
- A folder is left with no temp files after any run that finishes.
- A permanently broken file fails and rewrites its log on every run.
