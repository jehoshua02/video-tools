# 0014. download command via yt-dlp

## Status
Accepted. Extends the scope in [[0002-core-feature-scope]].

## Context
The user wants to save YouTube videos as mp4. yt-dlp defaults to webm/opus,
so a format selector is needed to get mp4 with m4a audio.

## Decision
- New command: `python -m video_tools download <url> [-o <folder>]`.
- Shell out to yt-dlp (same approach as [[0004-ffmpeg-subprocess-engine]]):
  `yt-dlp --no-playlist -f "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]" --merge-output-format mp4 -o "<folder>\%(title)s.%(ext)s" <url>`
- One URL per run. No playlists, no audio-only mode.
- Default folder is `~\Downloads`.
- yt-dlp output is shown live (progress bar); the command's exit code is yt-dlp's.
- install.ps1 installs yt-dlp via winget (`yt-dlp.yt-dlp`).

## Consequences
- Adds a runtime prerequisite (yt-dlp) and a network-dependent command.
- Re-running on the same URL is a no-op: yt-dlp skips files that already exist.
- Videos with no mp4 format available fail rather than falling back to webm.
- yt-dlp needs regular updates as YouTube changes (`winget upgrade yt-dlp.yt-dlp`).
