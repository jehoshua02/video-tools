# 0015. download prefers H.264 video

## Status
Accepted. Amends the format selector in [[0014-download-command]].

## Context
The `ext=mp4` selector can pick AV1 video inside mp4 (seen on the first real
download). AV1 won't play on older TVs and phones, and to-mp4 won't fix it
because the file is already `.mp4`.

## Decision
Format selector becomes:
`bv*[vcodec^=avc1]+ba[ext=m4a]/bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]`
- First choice: best H.264 (avc1) video + m4a audio.
- Fallback: the previous mp4 selector, if no H.264 stream exists.

## Consequences
- Downloads play almost everywhere.
- YouTube usually offers H.264 only up to 1080p, so higher resolutions are not used.
- A video with no H.264 stream can still come down as AV1/VP9 in mp4.
