# Log unreadable files that look like videos

## Abstract

Corrupt files ffprobe can't read (e.g. a broken `.mkv`) were silently ignored by to-mp4, with no error log.

## Priority

Not scored; user asked to build inbox items.

## Timeline

- Captured: 2026-09-16
- Started: 2026-09-16
- Verified: 2026-09-16
- Done: 2026-09-16

## Details

- Decision recorded in ADR 0013.
- If ffprobe fails and the extension is a common video type, write `<stem>.error.log` (ffprobe command + stderr) and count as failed.
- Unknown extensions that ffprobe can't read are still ignored silently.
- `probe()` now returns `(info, error_text)`; shared `write_error_log()` helper.

## Verification

- `python -m pytest`: 8 passed. New test: `broken.MKV` logged and failed (exit 1), `broken.dat` ignored.
- Manual rerun of the sample folder: `failed broken.mkv (see broken.error.log)`, 3 skipped, exit 1. Log shows ffprobe's "EBML header parsing failed / Invalid data" message.
