# 0016. No silent skips: every file ends as mp4 or error log

## Status
Accepted. Supersedes [[0013-log-unreadable-video-files]]. Amends [[0008-ffprobe-video-detection]].

## Context
to-mp4 silently ignored files it judged "not a video" (text, photos, audio,
unreadable files with unknown extensions). The user wants a binary outcome
with nothing ignored.

## Decision
After a run, every file in the folder has either a matching `<stem>.mp4` or a
`<stem>.error.log`. Specifically:
- Files ffprobe cannot read: error log with the ffprobe command and stderr.
- Files with no video stream (text, still images, audio): error log stating
  "Not a video" and the detected format.
- Both count as failed; the run exits non-zero.
- The extension list from ADR 0013 is removed; extensions no longer matter.

Only exceptions, which are never probed or logged: `.mp4` files and the tool's
own artifacts (`.error.log`, `.mp4.partial`). Files whose `<stem>.mp4` already
exists are reported as skipped (printed, not silent).

## Consequences
- Nothing is ignored; every outcome is visible in the folder and the output.
- Folders with non-video files (photos, notes) get an error log per file and
  always exit non-zero.
- Those logs are rewritten on every run until the files are removed.
