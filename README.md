# video-tools

Command-line video tools for Windows.

## Install

Requires Windows with git and winget.

```powershell
git clone https://github.com/jehoshua02/video-tools.git
cd video-tools
powershell -ExecutionPolicy Bypass -File install.ps1
```

The script installs Python 3.12+, ffmpeg and yt-dlp if missing, then verifies them. Open a new terminal afterwards.

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
- If a video fails, writes the error to `foo.error.log` next to it and moves on. Failed files are retried on the next run, and the log is removed once they convert.
- Files with a video extension that can't be read (corrupt) also count as failed and get an error log.
- Exits with a non-zero code if any file failed.

### download

Downloads a YouTube video as mp4.

```powershell
python -m video_tools download "https://www.youtube.com/watch?v=..."
python -m video_tools download "https://www.youtube.com/watch?v=..." -o "D:\Videos\Inbox"
```

- Saves to your Downloads folder unless `-o` is given. The file is named after the video title.
- Prefers H.264 video so it plays on most devices (usually up to 1080p).
- One video per run; playlist links download only the linked video.
- Skips the download if the file already exists.
- If downloads start failing, update yt-dlp: `winget upgrade yt-dlp.yt-dlp`

## Development

Run the tests:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install pytest
python -m pytest
```

Design decisions are recorded in [docs/plan/adrs](docs/plan/adrs).
