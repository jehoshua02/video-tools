import json
import shutil
import subprocess
from pathlib import Path

PARTIAL_SUFFIX = ".mp4.partial"
ERROR_SUFFIX = ".error.log"

# ffprobe reads plain text as "tty" and still images as image2/*_pipe.
NON_VIDEO_FORMATS = {"tty", "image2"}


def run(folder: Path) -> int:
    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            print(f"error: {tool} not found on PATH. Run install.ps1.")
            return 2
    if not folder.is_dir():
        print(f"error: not a folder: {folder}")
        return 2

    for p in folder.iterdir():
        if p.is_file() and p.name.lower().endswith(PARTIAL_SUFFIX):
            p.unlink()

    counts = {"converted": 0, "remuxed": 0, "skipped": 0, "failed": 0}
    files = sorted((p for p in folder.iterdir() if p.is_file()), key=lambda p: p.name.lower())
    for src in files:
        name = src.name.lower()
        if src.suffix.lower() == ".mp4" or name.endswith(ERROR_SUFFIX):
            continue

        target = src.with_suffix(".mp4")
        if target.exists():
            print(f"skipped    {src.name} ({target.name} exists)")
            counts["skipped"] += 1
            continue

        info = probe(src)
        video = pick_video_stream(info) if info else None
        if video is None:
            continue

        result = convert(src, target, info, video)
        counts[result] += 1

    print(
        f"\n{counts['converted']} converted, {counts['remuxed']} remuxed, "
        f"{counts['skipped']} skipped, {counts['failed']} failed"
    )
    return 1 if counts["failed"] else 0


def probe(src: Path) -> dict | None:
    proc = subprocess.run(
        ["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(src)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if proc.returncode != 0:
        return None
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return None


def pick_video_stream(info: dict) -> dict | None:
    fmt = info.get("format", {}).get("format_name", "")
    if fmt in NON_VIDEO_FORMATS or fmt.endswith("_pipe"):
        return None
    for s in info.get("streams", []):
        if s.get("codec_type") == "video" and not s.get("disposition", {}).get("attached_pic"):
            return s
    return None


def first_audio_stream(info: dict) -> dict | None:
    return next((s for s in info.get("streams", []) if s.get("codec_type") == "audio"), None)


def codec_args(info: dict, video: dict) -> tuple[str, list[str]]:
    audio = first_audio_stream(info)
    if video.get("codec_name") == "h264" and (audio is None or audio.get("codec_name") == "aac"):
        return "remuxed", ["-c", "copy"]
    return "converted", [
        "-c:v", "libx264", "-crf", "23", "-preset", "medium", "-pix_fmt", "yuv420p",
        "-c:a", "aac",
    ]


def convert(src: Path, target: Path, info: dict, video: dict) -> str:
    partial = src.with_name(target.name + ".partial")
    log = src.with_name(src.stem + ERROR_SUFFIX)
    kind, codecs = codec_args(info, video)
    cmd = [
        "ffmpeg", "-hide_banner", "-nostdin", "-y",
        "-i", str(src),
        "-map", f"0:{video['index']}", "-map", "0:a:0?",
        *codecs,
        "-movflags", "+faststart",
        "-f", "mp4", str(partial),
    ]

    ok = False
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if proc.returncode == 0:
            partial.replace(target)
            ok = True
    finally:
        if not ok:
            partial.unlink(missing_ok=True)

    if ok:
        log.unlink(missing_ok=True)
        print(f"{kind:<10} {src.name} -> {target.name}")
        return kind

    log.write_text(
        f"command: {subprocess.list2cmdline(cmd)}\nexit code: {proc.returncode}\n\n{proc.stderr}",
        encoding="utf-8",
    )
    print(f"failed     {src.name} (see {log.name})")
    return "failed"
