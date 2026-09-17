# README: curl option shows errors; browser option handles .txt name

## Abstract

Fix two README install options that failed confusingly on another user's computer.

## Priority

Not scored; found from a user's failing install.

## Timeline

- Captured: 2026-09-17
- Started: 2026-09-17
- Verified: 2026-09-17
- Done: 2026-09-17

## Details

- On the affected computer: jsDelivr via `irm` failed to connect; the curl option ended with iex "Cannot bind argument to parameter 'Command' because it is an empty string" because `-s` hid curl's error; the browser option failed with "file does not exist", most likely saved as `install.ps1.txt`.
- Browser works there but PowerShell and curl don't: points to a DNS filter (browser secure DNS bypasses it), security software, or a firewall. Asked the user for `Resolve-DnsName` and `curl.exe -I` output; not yet received.
- README changes: curl option uses `-sSL` and prints "Download failed" instead of an iex error; browser option says "Save as type: All files" and how to find/rename `install.ps1.txt`; troubleshooting mentions DNS filters and `Resolve-DnsName`.
- If command-line network access stays blocked, winget and git will fail too; that must be fixed on that machine.

## Verification

- New curl command against an unreachable address: prints `curl: (7) Failed to connect...` then "Download failed. See the curl error above."
- New curl command against the real URL (scratch home folder): `OK video-tools command`, "All set".
- User PATH restored afterwards.
