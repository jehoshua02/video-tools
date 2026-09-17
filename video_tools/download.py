import shutil
import subprocess
from pathlib import Path

FORMAT = "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]"


def build_command(url: str, folder: Path) -> list[str]:
    return [
        "yt-dlp", "--no-playlist",
        "-f", FORMAT,
        "--merge-output-format", "mp4",
        "-o", str(folder / "%(title)s.%(ext)s"),
        url,
    ]


def run(url: str, folder: Path | None = None) -> int:
    for tool in ("yt-dlp", "ffmpeg"):
        if not shutil.which(tool):
            print(f"error: {tool} not found on PATH. Run install.ps1.")
            return 2
    folder = folder or Path.home() / "Downloads"
    if not folder.is_dir():
        print(f"error: not a folder: {folder}")
        return 2
    return subprocess.run(build_command(url, folder)).returncode
