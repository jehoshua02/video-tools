# README: other install options and troubleshooting

## Abstract

Add curl and browser-download install options, plus a troubleshooting section, to the README.

## Priority

Not scored; user asked for it directly.

## Timeline

- Captured: 2026-09-17
- Started: 2026-09-17
- Verified: 2026-09-17
- Done: 2026-09-17

## Details

- Trigger: on another user's computer `irm` failed with "Unable to connect to the remote server" for both raw.githubusercontent.com and jsDelivr, while the same URL opened fine in the browser. So PowerShell itself is blocked from the internet there (security software or firewall), not the site.
- README now has "Other ways to install" (curl.exe, browser download + `-File`, jsDelivr) and "Troubleshooting" (download blocked, winget/git blocked, launcher missing, command not recognized, non-install folder, missing dependencies, failed conversions, failing downloads).
- Not yet known whether curl.exe or the browser option worked on that computer.

## Verification

- curl.exe option run in a fresh session with `$HOME` pointed at a scratch folder: cloned, `OK video-tools command`, "All set".
- Saved-file option (`install.ps1` in `<home>\Downloads`, run with `-ExecutionPolicy Bypass`): same result.
- User PATH restored to its original value afterwards.
