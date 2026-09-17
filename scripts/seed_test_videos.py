"""Create a folder of small dummy files for trying out `to-mp4`."""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

VIDEO = ["-f", "lavfi", "-i", "testsrc=duration=2:size=320x240:rate=25"]
AUDIO = ["-f", "lavfi", "-i", "sine=frequency=440:duration=2"]

# name -> ffmpeg args after the inputs (None audio codec = no audio track)
VIDEOS = {
    "avi mpeg4 mp3.avi": ("mpeg4", "libmp3lame"),
    "flv flash.flv": ("flv1", "libmp3lame"),
    "mkv h264 aac (remux).mkv": ("libx264", "aac"),
    "mkv h264 ac3.mkv": ("libx264", "ac3"),
    "mov no audio.mov": ("mpeg4", None),
    "mpg mpeg2.mpg": ("mpeg2video", "mp2"),
    "ts h264 aac (remux).ts": ("libx264", "aac"),
    "UPPERCASE EXT.MKV": ("libx264", "aac"),
    "webm vp9 opus.webm": ("libvpx-vp9", "libopus"),
    "wmv windows media.wmv": ("wmv2", "wmav2"),
    "ünïcödé name.avi": ("mpeg4", "libmp3lame"),
    "already converted.mp4": ("libx264", "aac"),
    "same name clash.avi": ("mpeg4", "libmp3lame"),
    "same name clash.mkv": ("libx264", "aac"),
}


def ffmpeg(*args: str) -> None:
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args], check=True)


def make_video(path: Path, vcodec: str, acodec: str | None) -> None:
    args = [*VIDEO]
    if acodec:
        args += [*AUDIO, "-c:a", acodec]
    ffmpeg(*args, "-c:v", vcodec, "-pix_fmt", "yuv420p", str(path))


def seed(folder: Path) -> None:
    for name, (vcodec, acodec) in VIDEOS.items():
        make_video(folder / name, vcodec, acodec)
        print(f"video  {name}")

    ffmpeg("-f", "lavfi", "-i", "testsrc=duration=1:size=160x120:rate=5", str(folder / "animated.gif"))
    print("video  animated.gif")

    # Files below should each end with an .error.log
    (folder / "error corrupt.mkv").write_bytes(b"\x00\x01 this is not a video " * 200)

    (folder / "error empty.mov").write_bytes(b"")

    # mov keeps its index at the end, so cutting the file in half makes it unreadable
    whole = folder / "error truncated.mov"
    make_video(whole, "mpeg4", "aac")
    data = whole.read_bytes()
    whole.write_bytes(data[: len(data) // 2])

    (folder / "error notes.txt").write_text("Just some notes, not a video.\n", encoding="utf-8")
    ffmpeg("-f", "lavfi", "-i", "color=blue:size=64x64", "-frames:v", "1", str(folder / "error photo.jpg"))
    ffmpeg(*AUDIO, str(folder / "error song.mp3"))
    for name in ("corrupt.mkv", "empty.mov", "truncated.mov", "notes.txt", "photo.jpg", "song.mp3"):
        print(f"error  error {name}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", nargs="?", type=Path, default=Path("test-videos"))
    parser.add_argument("--force", action="store_true", help="delete the folder first if it exists")
    args = parser.parse_args()

    if not shutil.which("ffmpeg"):
        print("error: ffmpeg not found on PATH. Run install.ps1.")
        return 2
    if args.folder.exists() and any(args.folder.iterdir()):
        if not args.force:
            print(f"error: {args.folder} is not empty. Use --force to delete and recreate it.")
            return 2
        shutil.rmtree(args.folder)
    args.folder.mkdir(parents=True, exist_ok=True)

    seed(args.folder)
    print(f"\nSeeded {args.folder}. Try: python -m video_tools to-mp4 \"{args.folder}\"")
    return 0


if __name__ == "__main__":
    sys.exit(main())
