# video-tools on PATH, plus update command

## Abstract

`video-tools <command>` works from any folder; `video-tools update` pulls the latest version.

## Priority

Not scored; user asked for it directly.

## Timeline

- Captured: 2026-09-16
- Started: 2026-09-16
- Verified: 2026-09-16
- Done: 2026-09-16

## Details

- User chose the launcher approach over `pip install -e .`. Recorded in ADR 0017.
- `bin\video-tools.cmd`, `video_tools/update.py`, PATH step + check in `install.ps1`, `.gitattributes` for CRLF.
- argparse `prog` is now `video-tools`.
- install.ps1 no longer `cd`s into the repo: with the command on PATH there's no need, and the user stays where they were.
- Bugs found while testing, both fixed:
  - Ending the launcher with `& exit /b` lost the exit code (always 0). Fix: make `python` the last command.
  - "Updating..." printed after git's output when stdout was piped. Fix: `flush=True`.

## Verification

- `python -m pytest`: 18 passed (4 new update tests).
- `install.ps1` from the repo: "Adding ...\bin to your PATH", `OK video-tools command`, exit 0. Rerun: "video-tools already on PATH". User PATH contains the entry once.
- From another folder with a fresh PATH: `video-tools --help` works (exit 0); `to-mp4 nope` exits 2; `to-mp4 e2e` (failed files) exits 1; same exit 2 from cmd.exe.
- `video-tools update` from another folder: "Updating C:\...\video-tools... Already up to date.", exit 0.
- Not tested: the iex one-liner with the PATH step (it would add a scratch folder to the real user PATH); a pull that rewrites the launcher mid-run.
