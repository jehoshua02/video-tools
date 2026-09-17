# install.ps1 replaces older video-tools PATH entries

## Abstract

Installing a second copy used to add a second PATH entry, and the older copy won. Now the latest install is the only one on PATH.

## Priority

Not scored; user asked for it directly.

## Timeline

- Captured: 2026-09-17
- Started: 2026-09-17
- Verified: 2026-09-17
- Done: 2026-09-17

## Details

- Found when the user was about to run the one-liner on a machine whose PATH already had the dev repo's `bin`.
- An entry counts as an older install if it ends in `\video-tools\bin` (covers deleted folders) or the folder contains `video-tools.cmd`.
- Recorded as an addition to ADR 0017.
- Context: the user's one-liner error ("Cannot bind argument to parameter 'Path'") was the pre-PR-#3 install.ps1 served from GitHub's raw cache; the current script runs fine via `irm | iex`.

## Verification

- Scratch standalone install: "Removing older video-tools PATH entry: ...\dev\...\bin", added scratch entry, `OK video-tools command`.
- Then `install.ps1` from the dev repo: removed the scratch entry, re-added the dev entry.
- Third run: "video-tools already on PATH."
- User PATH after the three runs was identical to the PATH before them.
