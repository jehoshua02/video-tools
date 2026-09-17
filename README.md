# video-tools

Command-line video tools for Windows.

## Prerequisites

- **Windows**
- **Python 3.12+** — `winget install Python.Python.3.12`
- **ffmpeg and ffprobe** — `winget install Gyan.FFmpeg`
- **git** — `winget install Git.Git`

Open a new terminal after installing so the tools are on your PATH. Check:

```powershell
python --version
ffmpeg -version
ffprobe -version
```

## Install

No install step. Clone the repo:

```powershell
git clone https://github.com/jehoshua02/video-tools.git
cd video-tools
```

## Tools

Run each tool from the repo folder.

### to-mp4

Converts every video in a folder to mp4.

```powershell
python -m video_tools to-mp4 "D:\Videos\Inbox"
```

- Scans only the given folder, not subfolders.
- Leaves originals in place. `foo.mkv` becomes `foo.mp4` next to it.
- Safe to re-run. Skips files that are already `.mp4` or already have a matching `.mp4`.
- Copies H.264/AAC videos into mp4 without re-encoding (fast, no quality loss). Re-encodes everything else to H.264/AAC.
- If a video fails, writes the error to `foo.error.log` next to it and moves on. Fixed files are retried on the next run, and the log is removed once they convert.
- Exits with a non-zero code if any file failed.

## Development

Run the tests:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install pytest
python -m pytest
```

Design decisions are recorded in [docs/plan/adrs](docs/plan/adrs).
