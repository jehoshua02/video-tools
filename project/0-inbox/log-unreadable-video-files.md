# Log unreadable files that look like videos

## Abstract

Corrupt files ffprobe can't read (e.g. a broken `.mkv`) are silently ignored by to-mp4, with no error log.

## Timeline

- Captured: 2026-09-16

## Details

ADR 0008 detects videos with ffprobe only, so an unreadable file looks the same as a non-video file.
Option: if ffprobe fails and the extension is a common video type (mkv, avi, mov, wmv, flv, webm, m4v, mpg, ts), write `<stem>.error.log` and count it as failed.
