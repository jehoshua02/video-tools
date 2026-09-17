# video-tools

Command-line video tools for Windows.

## Install

Requires Windows 10 or 11 (winget is built in). In a normal PowerShell window (not "Run as administrator"):

```powershell
irm https://raw.githubusercontent.com/jehoshua02/video-tools/main/install.ps1 | iex
```

This runs the install script, which:

- installs git, Python 3.12+, ffmpeg and yt-dlp if missing
- clones the tools into `video-tools` in your home folder (`C:\Users\<you>\video-tools`), or updates them if already there
- adds the `video-tools` command to your PATH, so it works from any folder (replacing the PATH entry of any earlier install)
- verifies everything

Then try `video-tools --help`. If the command isn't found, open a new terminal.

To uninstall, delete `C:\Users\<you>\video-tools` and remove its `bin` folder from your user PATH.

### Other ways to install

If the command above can't download the script, try these in order. They all run the same install script.

**Option 2: download with curl.** `curl.exe` is built into Windows and is often allowed when PowerShell's own downloader is blocked:

```powershell
iex (curl.exe -sL https://raw.githubusercontent.com/jehoshua02/video-tools/main/install.ps1 | Out-String)
```

**Option 3: download with your browser.** Open [install.ps1](https://raw.githubusercontent.com/jehoshua02/video-tools/main/install.ps1), press Ctrl+S, and save it as `install.ps1` in your Downloads folder. Then run:

```powershell
powershell -ExecutionPolicy Bypass -File $HOME\Downloads\install.ps1
```

**Option 4: download from a different site**, if your network blocks `raw.githubusercontent.com` (the copy here can be a few hours behind):

```powershell
irm https://cdn.jsdelivr.net/gh/jehoshua02/video-tools@main/install.ps1 | iex
```

### Troubleshooting

**"Unable to connect to the remote server" when running the install command.** The script never ran; the download was blocked.

1. Open the [install.ps1 link](https://raw.githubusercontent.com/jehoshua02/video-tools/main/install.ps1) in a browser on the same computer.
2. If the browser shows the script: your network is fine, and security software or a firewall is blocking PowerShell from the internet. Use Option 2, then Option 3.
3. If the browser can't open it either: your network is blocking the site. Turn off any VPN or web filter, try Option 4, or use another network such as a phone hotspot.
4. To check the connection from PowerShell, run `Test-NetConnection raw.githubusercontent.com -Port 443`. `TcpTestSucceeded : True` means the site is reachable.

Running PowerShell as administrator does not fix this, and isn't needed for any part of the install.

**The script runs, but winget or the git download fails with a connection error.** The same security software is blocking command-line tools in general. Allow them, or pause the protection while you install.

**"FAIL video-tools command not found".** The line says whether the launcher file is missing. If it is, delete `C:\Users\<you>\video-tools` and run the install again.

**"video-tools is not recognized" after a successful install.** Open a new terminal, so it picks up the updated PATH.

**"already exists but is not a video-tools install".** A different `video-tools` folder is in your home folder. Rename or delete it, then run the install again.

**The install ends with "Some dependencies are missing".** Open a new terminal and run the install command again. It is safe to repeat; it skips what is already installed.

**A video fails to convert.** Open the `.error.log` file next to it; it contains the exact ffmpeg error.

**`video-tools download` starts failing.** YouTube changes often. Update the downloader: `winget upgrade yt-dlp.yt-dlp`

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
