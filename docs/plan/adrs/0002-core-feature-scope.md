# 0002. Initial feature scope

## Status
Accepted

## Context
Need to bound v1 scope for the CLI rather than build a general editor.

## Decision
First release covers three capability areas:
- Transcode/convert & compress (format, codec, bitrate, presets)
- Batch processing & watch-folder (process many files, watch a directory for new files)
- Metadata/inspection (probe codec/duration/resolution, thumbnails/reports)

Trim/cut & concat is explicitly deferred to a later release.

## Consequences
- v1 has no timeline-editing features (cut/concat).
- Batch/watch-folder implies a long-running mode, not just one-shot invocations.
