# 0004. ffmpeg/ffprobe via subprocess as processing engine

## Status
Accepted

## Context
Transcode, compress, and metadata features need an underlying video engine.
Options considered: shell out to ffmpeg/ffprobe binaries, or use PyAV bindings.

## Decision
Shell out to ffmpeg/ffprobe binaries as subprocesses.

## Consequences
- Requires ffmpeg/ffprobe installed and on PATH; CLI should check and fail with a clear error if missing.
- Avoids a heavy compiled Python dependency (PyAV).
- Access to full ffmpeg CLI flag surface for presets/codecs.
