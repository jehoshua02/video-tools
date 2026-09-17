# 0017. `video-tools` command on PATH, and an update command

## Status
Accepted. Amends [[0011-project-tooling]] (how the tool is run) and [[0003-local-cli-distribution]].

## Context
Users had to `cd` into the install folder and type `python -m video_tools ...`,
and update by running `git pull` there.

## Decision
- `bin\video-tools.cmd` launches the repo's code: it sets `PYTHONPATH` to the
  repo and runs `python -m video_tools`. No pip install, no packaging.
- `install.ps1` adds the repo's `bin` folder to the **user** PATH (no admin rights).
- Only one install is on PATH at a time: `install.ps1` removes user PATH entries
  from other video-tools installs (entries ending in `\video-tools\bin`, or
  folders containing `video-tools.cmd`), so the latest install wins.
- New command `video-tools update` runs `git pull --ff-only` in the install folder.
- Chosen over `pyproject.toml` + `pip install -e .`: no pip step, and pip's
  Scripts folder is often missing from PATH on Windows.

Launcher constraints:
- The work is on a single line, because cmd re-reads a batch file after each
  line and `update` may rewrite the launcher while it runs.
- `python` is the last command on that line so its exit code is the launcher's.
- `.gitattributes` forces CRLF for `*.cmd`.

## Consequences
- `video-tools <command>` works from any folder; `python -m video_tools` still works from the repo.
- Install now makes a lasting change to the machine (a user PATH entry). Uninstall = delete the folder and that PATH entry.
- `update` needs a git clone; it refuses to run in a zip download.
- `update` does not install new dependencies; re-run `install.ps1` if a later version needs any.
- Moving the install folder breaks the PATH entry until `install.ps1` is re-run.
