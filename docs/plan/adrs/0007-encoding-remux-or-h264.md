# 0007. Remux when compatible, else H.264/AAC

## Status
Accepted

## Context
Need default encoding for mp4 output. Tradeoff: speed and quality vs consistency.

## Decision
Probe streams with ffprobe:
- Video is H.264 and audio is AAC (or absent): remux with `-c copy`.
- Otherwise: re-encode video with `libx264 -crf 23 -preset medium`, audio with `aac`.
- Always add `-movflags +faststart`.

## Consequences
- Compatible files convert in seconds with no quality loss.
- Mixed cases (e.g. H.264 video + AC3 audio) re-encode both streams in v1; per-stream copy is a later refinement.
- Subtitles and extra streams are not carried over in v1.
