# README: manual install steps; launcher shadowing fix

## Abstract

Add plain-command install steps (winget, git clone, PATH) to the README, for computers where the install script can't be downloaded.

## Priority

Not scored; user asked for it directly.

## Timeline

- Captured: 2026-09-17
- Started: 2026-09-17
- Verified: 2026-09-17
- Done: 2026-09-17

## Details

- Trigger: another user's computer blocks PowerShell and curl downloads, so none of the script-based options worked.
- README "Manual install": four winget installs, `git clone` into `~\video-tools`, one PATH command, a check command, and a browser zip fallback when `git clone` can't connect (no `video-tools update` that way).
- Bug found while testing: the launcher ran whatever `video_tools` folder was in the current folder instead of its own install, because `python -m` puts the current folder first on the import path. Fix: `python -P` (Python 3.11+; we require 3.12). Added to ADR 0017.
- Open risk: on that computer winget and git may be blocked too; then only fixing the block (DNS filter, security software, firewall) helps.

## Verification

- Zip route in a scratch home folder: `Expand-Archive` + `ren` gives `video-tools\bin\video-tools.cmd`; `--help` works; `update` correctly refuses ("not a git clone") and names the scratch install, proving the launcher uses its own code even when run from the dev repo folder; `to-mp4 nope` exits 2.
- PATH command expression evaluated (not applied): appends `<home>\video-tools\bin`.
- Dev launcher: `update` reports the dev repo, exit 0. `python -m pytest`: 18 passed.
