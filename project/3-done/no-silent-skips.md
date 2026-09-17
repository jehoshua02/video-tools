# No silent skips in to-mp4

## Abstract

Every file ends as an mp4 or an error log; nothing is silently ignored.

## Priority

Not scored; user asked for it directly.

## Timeline

- Captured: 2026-09-16
- Started: 2026-09-16
- Verified: 2026-09-16
- Done: 2026-09-16

## Details

- User: "I don't want any silent skips. mp4 or error log. Binary outcome."
- Recorded in ADR 0016 (supersedes 0013).
- Non-videos (text, images, audio) and unreadable files all get `<stem>.error.log` and count as failed.
- Removed the `VIDEO_EXTENSIONS` list; extensions no longer matter.
- Never probed: `.mp4` files, `.error.log`, `.mp4.partial`.

## Verification

- `python -m pytest`: 14 passed. New tests: avi/corrupt mkv/txt/png/mp3 folder gives 1 mp4 + 4 error logs, exit 1; rerun doesn't process error logs.
- Manual run on the sample folder: jpg, mp3 and corrupt mkv each got an error log ("Not a video: ... jpeg_pipe"), 3 skipped (mp4 exists), exit 1.
