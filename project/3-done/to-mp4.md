# to-mp4 batch converter

## Abstract

`python -m video_tools to-mp4 <folder>` converts every video in a folder to mp4, idempotently.

## Priority

Not scored (only task; user asked to just build).

## Timeline

- Captured: 2026-09-16
- Started: 2026-09-16
- Verified: 2026-09-16
- Done: 2026-09-16

## Details

Decisions in docs/plan/adrs 0005–0012.

- Code: `video_tools/cli.py` (argparse), `video_tools/to_mp4.py` (logic).
- Not-video rule: ffprobe fails, format is `tty` (text), `image2` or `*_pipe` (still images), or the only video stream is cover art (`attached_pic`).
- Animated gifs count as video and get converted.
- ffprobe failure = not a video, so corrupt videos are silently ignored. Follow-up in `0-inbox/log-unreadable-video-files.md`.
- Only the first video stream and first audio stream are kept.
- Re-encode adds `-pix_fmt yuv420p` for player compatibility.
- Files with the same stem (`foo.mkv`, `foo.avi`) share `foo.mp4` and `foo.error.log`; the first alphabetically wins.

## Verification

- `python -m pytest`: 7 passed. Covers re-encode, remux, no-audio, ignoring txt/png, rerun no-op (mtimes unchanged), uppercase `.MP4` target, leftover `.partial` cleanup, failure log + continue + exit 1, stale log removal, missing folder.
- Manual run on avi (mpeg4/mp3), webm (vp9), gif, jpg, mp3, corrupt mkv: 3 converted, jpg/mp3/corrupt ignored, exit 0. Rerun: 3 skipped, exit 0, no temp files left.
