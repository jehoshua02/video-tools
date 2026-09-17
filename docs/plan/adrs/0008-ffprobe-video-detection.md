# 0008. Detect video files with ffprobe

## Status
Accepted

## Context
Folder may hold unknown or unusual video extensions. Need to decide which files to convert.

## Decision
Run ffprobe on every non-skipped file. Treat it as video when ffprobe succeeds
and reports at least one video stream that is not a still image
(exclude `attached_pic` and single-frame image codecs like png/mjpeg with no duration).

## Consequences
- Catches any format ffmpeg can read, regardless of extension.
- Slower on folders with many non-video files (one ffprobe call each).
- Image-filtering rule may need tuning after real-world runs.
