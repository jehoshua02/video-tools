# Install into the home folder, not the current folder

## Abstract

The one-liner cloned into whatever folder the user was in, which could be `C:\Windows` in an administrator shell. It now always uses `~\video-tools`.

## Priority

Not scored; user approved it directly.

## Timeline

- Captured: 2026-09-17
- Started: 2026-09-17
- Verified: 2026-09-17
- Done: 2026-09-17

## Details

- Trigger: a user on another computer got "Unable to connect to the remote server" from `irm` (network block of raw.githubusercontent.com, not a script bug). Their screenshot showed `cd ..` before the command, consistent with an admin shell starting in `System32`. Running as administrator doesn't help that error and makes the install location dangerous.
- `install.ps1`: standalone mode uses `Join-Path $HOME 'video-tools'`. In-repo mode unchanged.
- The "Removing older PATH entry" message now says the old folder can be deleted, since earlier installs may live elsewhere.
- README: says to use a normal (non-admin) window, names the install location, and adds a jsDelivr fallback command for networks that block raw.githubusercontent.com.
- Caveat: jsDelivr caches `@main` for up to about 12 hours, so the fallback can serve a slightly older install.ps1. It still clones the latest repo.
- Recorded as an addition to ADR 0017.

## Verification

- Ran the script via `iex` with cwd `C:\Windows\System32` and `$HOME` pointed at a scratch folder: cloned into `<home>\video-tools`, `OK video-tools command`, nothing created in System32, cwd unchanged.
- Second run: "already exists; updating it...", "video-tools already on PATH".
- User PATH restored to its original value afterwards.
- jsDelivr and api.github.com URLs both returned the current install.ps1 (5782 bytes) on 2026-09-17.
