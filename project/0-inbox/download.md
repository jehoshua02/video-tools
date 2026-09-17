# download command

## Abstract

`python -m video_tools download <url>` saves a YouTube video as mp4 via yt-dlp.

## Priority: XX

## Timeline

- Captured: 2026-09-16

## Details

- Working manual command:
  `yt-dlp -f "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]" --merge-output-format mp4 -o "$HOME\Downloads\%(title)s.%(ext)s" <url>`
- Default format gives webm (opus audio); the format selector above forces mp4/m4a.
- Needs yt-dlp (winget `yt-dlp.yt-dlp`); not yet in install.ps1.
- Outside ADR 0002 scope (convert, batch, inspect) — needs new ADR.

## Verification
