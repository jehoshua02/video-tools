# 0005. First deliverable: idempotent batch-to-mp4 script

## Status
Accepted

## Context
Need a concrete, minimal first slice within the scope set by [[0002-core-feature-scope]].

## Decision
First deliverable is a batch script: point it at a folder, convert every video
file found to mp4 (via ffmpeg, per [[0004-ffmpeg-subprocess-engine]]). It is
idempotent — files already in mp4 form are left alone, safe to re-run on the
same folder repeatedly.

Skip detection is by file extension: any file already named `.mp4` is left
alone, no ffprobe container check.

## Consequences
- Simple and fast; a mislabeled non-mp4 file with an `.mp4` extension would be
  skipped incorrectly (accepted tradeoff).
- No watch-folder or CLI flags required yet — one-shot folder scan.
- Establishes the ffmpeg invocation pattern reused by later transcode features.
