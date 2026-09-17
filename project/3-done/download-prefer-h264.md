# download prefers H.264

## Abstract

Make `download` pick H.264 video first, since the mp4 selector can return AV1.

## Priority

Not scored; user asked for it directly.

## Timeline

- Captured: 2026-09-16
- Started: 2026-09-16
- Verified: 2026-09-16
- Done: 2026-09-16

## Details

- User chose "Prefer H.264" after the first real download came back AV1.
- Recorded in ADR 0015. Selector: `bv*[vcodec^=avc1]+ba[ext=m4a]/bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]`.
- Keeps the old selector as fallback, so videos without H.264 still download.

## Verification

- `python -m pytest`: 13 passed.
- Real download of https://www.youtube.com/watch?v=jNQXAC9IVRw: yt-dlp picked format 18, output `Me at the zoo.mp4` is h264 + aac, exit 0 (previously av1 + aac).
