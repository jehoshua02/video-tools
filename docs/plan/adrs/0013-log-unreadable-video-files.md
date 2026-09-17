# 0013. Log unreadable files with video extensions

## Status
Superseded by [[0016-no-silent-skips]]. Amended [[0008-ffprobe-video-detection]].

## Context
With ffprobe-only detection, a corrupt video (e.g. a broken `.mkv`) looks the
same as a non-video file and is silently ignored. The user never learns it failed.

## Decision
When ffprobe cannot read a file:
- If its extension is a common video type (3gp, asf, avi, divx, f4v, flv, m2ts,
  m4v, mkv, mov, mpeg, mpg, mts, ogv, ts, vob, webm, wmv; case-insensitive),
  write the ffprobe command and stderr to `<stem>.error.log` and count it as failed.
- Otherwise, ignore it silently as before.

Files ffprobe can read are still judged by their streams, not their extension.

## Consequences
- Corrupt videos show up as failures with a log, and the run exits non-zero.
- A corrupt file with an unusual extension is still silently ignored.
- A permanently corrupt file fails on every run until the user removes it.
