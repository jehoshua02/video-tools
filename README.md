# video-tools

Command-line video tools for Windows.

## Install

Requires Windows 10 or 11 (winget is built in). In PowerShell, from the folder where you want the tools:

```powershell
irm https://raw.githubusercontent.com/jehoshua02/video-tools/main/install.ps1 | iex
```

This runs the install script, which:

- installs git, Python 3.12+, ffmpeg and yt-dlp if missing
- clones the tools into a `video-tools` folder
- adds the `video-tools` command to your PATH, so it works from any folder
- verifies everything

Then try `video-tools --help`. If the command isn't found, open a new terminal.

To uninstall, delete the `video-tools` folder and remove its `bin` folder from your user PATH.

## Tools

### to-mp4

Converts every video in a folder to mp4.

```powershell
video-tools to-mp4 "D:\Videos\Inbox"
```

- Scans only the given folder, not subfolders.
- Leaves originals in place. `foo.mkv` becomes `foo.mp4` next to it.
- Safe to re-run. Skips files that are already `.mp4` or already have a matching `.mp4`.
- Copies H.264/AAC videos into mp4 without re-encoding (fast, no quality loss). Re-encodes everything else to H.264/AAC.
- If a video fails, writes the error to `foo.error.log` next to it and moves on. Failed files are retried on the next run, and the log is removed once they convert.
- Nothing is silently ignored: every file ends up with a matching `.mp4` or a `.error.log`. Files that aren't videos (photos, text, audio) or can't be read also get an error log and count as failed.
- Exits with a non-zero code if any file failed.

To try it safely first, create a folder of dummy files (various formats, plus files that should fail). Run this from inside the `video-tools` install folder:

```powershell
python scripts\seed_test_videos.py            # creates .\test-videos
python scripts\seed_test_videos.py --force    # delete and recreate it
video-tools to-mp4 test-videos
```

Files named `error ...` should each end with an `.error.log`; everything else should end with an `.mp4`.

### download

Downloads a YouTube video as mp4.

```powershell
video-tools download "https://www.youtube.com/watch?v=..."
video-tools download "https://www.youtube.com/watch?v=..." -o "D:\Videos\Inbox"
```

- Saves to your Downloads folder unless `-o` is given. The file is named after the video title.
- Prefers H.264 video so it plays on most devices (usually up to 1080p).
- One video per run; playlist links download only the linked video.
- Skips the download if the file already exists.
- If downloads start failing, update yt-dlp: `winget upgrade yt-dlp.yt-dlp`

### update

Updates video-tools to the latest version, from any folder.

```powershell
video-tools update
```

## Development

From the install folder, `python -m video_tools ...` runs the code directly, without the PATH launcher.

Run the tests:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install pytest
python -m pytest
```

Design decisions are recorded in [docs/plan/adrs](docs/plan/adrs).
