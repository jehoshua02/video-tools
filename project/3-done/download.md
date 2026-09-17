# download command

## Abstract

`python -m video_tools download <url>` saves a YouTube video as mp4 via yt-dlp.

## Priority: 43 (proposed; not confirmed, user asked to build inbox items)

- Value: 6/10 — handy, but not core to the convert/batch/inspect scope.
- Momentum: 2/10 — new, and separate from to-mp4.
- Effort: 3/10 — small yt-dlp wrapper, installer line, README, ADR.
- Risk: 2/10 — new command only; existing tools untouched.

## Timeline

- Captured: 2026-09-16
- Started: 2026-09-16
- Verified: 2026-09-16
- Done: 2026-09-16

## Details

- Working manual command:
  `yt-dlp -f "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]" --merge-output-format mp4 -o "$HOME\Downloads\%(title)s.%(ext)s" <url>`
- Default format gives webm (opus audio); the format selector above forces mp4/m4a.
- Needs yt-dlp (winget `yt-dlp.yt-dlp`); not yet in install.ps1.
- Decisions (2026-09-16):
  - Build after to-mp4 is done.
  - One URL per run. No playlists or audio-only mode.
  - Saves to ~/Downloads by default; optional `-o <folder>` to pick another.
  - Add yt-dlp to install.ps1.
- Outside ADR 0002 scope (convert, batch, inspect) — recorded in ADR 0014.
- Code: `video_tools/download.py`; `download` subcommand in `cli.py`.
- Added `--no-playlist` so playlist links fetch only the linked video.
- yt-dlp output streams live (no capture) so the progress bar shows.
- Also checks ffmpeg is on PATH, since yt-dlp needs it to merge video + audio.
- Finding: the `ext=mp4` selector can pick AV1 video (e.g. format 395). Plays in modern players, but not on older devices. Open question for the user: prefer H.264 (`vcodec^=avc1`)?

## Verification

- `python -m pytest`: 13 passed (5 new download tests; yt-dlp mocked).
- install.ps1: reports `OK yt-dlp 2026.08.19` (yt-dlp was already installed, so the winget install path wasn't exercised).
- Real download of https://www.youtube.com/watch?v=jNQXAC9IVRw to a scratch folder: `Me at the zoo.mp4` (av1 + aac), exit 0, temporary .f395/.f140 parts deleted.
- Rerun: "has already been downloaded", exit 0.
