# install.ps1 updates an existing clone instead of skipping it

## Abstract

On another user's computer the install ended with "FAIL video-tools command not found". An existing, outdated `video-tools` folder was being skipped instead of updated.

## Priority

Not scored; bug reported by the user.

## Timeline

- Captured: 2026-09-17
- Started: 2026-09-17
- Verified: 2026-09-17
- Done: 2026-09-17

## Details

- Likely cause (not confirmed on the other computer): an earlier one-liner run had cloned a version without `bin\video-tools.cmd`. Later runs printed "already exists; skipping download", so the launcher never arrived and the PATH check failed.
- Fix: if `video-tools\.git` exists, run `git pull --ff-only`; if the folder exists but isn't a clone, stop with a clear message.
- The FAIL line now says whether the launcher file is missing or present, to make remote reports diagnosable.
- To confirm on the other computer: the failing run's output should contain "already exists; skipping download".

## Verification

- Scratch folder with a clone reset to b5d900b (no `bin`):
  - main's script: "already exists; skipping download" then "FAIL video-tools command not found" (reproduced).
  - fixed script: "already exists; updating it..." then `OK video-tools command`, "All set".
- Folder named `video-tools` that isn't a clone: stops with "already exists but is not a video-tools install".
- User PATH restored to its original value after the tests.
