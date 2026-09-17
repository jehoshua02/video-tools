import json
import subprocess
from pathlib import Path

import pytest

from video_tools import to_mp4


def ffmpeg(*args: str) -> None:
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args], check=True)


def make_video(path: Path, vcodec: str, acodec: str | None) -> Path:
    args = ["-f", "lavfi", "-i", "testsrc=duration=1:size=64x64:rate=10"]
    if acodec:
        args += ["-f", "lavfi", "-i", "sine=duration=1", "-c:a", acodec]
    ffmpeg(*args, "-c:v", vcodec, "-pix_fmt", "yuv420p", str(path))
    return path


def codecs(path: Path) -> dict[str, str]:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", str(path)],
        capture_output=True, text=True, check=True,
    ).stdout
    return {s["codec_type"]: s["codec_name"] for s in json.loads(out)["streams"]}


@pytest.fixture
def folder(tmp_path: Path) -> Path:
    make_video(tmp_path / "a_reencode.avi", "mpeg4", "mp3")
    make_video(tmp_path / "b_remux.mkv", "libx264", "aac")
    make_video(tmp_path / "c_noaudio.mov", "mpeg4", None)
    make_video(tmp_path / "already.mp4", "libx264", "aac")
    return tmp_path


def test_converts_videos(folder: Path, capsys):
    assert to_mp4.run(folder) == 0

    assert codecs(folder / "a_reencode.mp4") == {"video": "h264", "audio": "aac"}
    assert codecs(folder / "b_remux.mp4") == {"video": "h264", "audio": "aac"}
    assert codecs(folder / "c_noaudio.mp4") == {"video": "h264"}
    assert not list(folder.glob("*.partial"))
    assert not list(folder.glob("*.error.log"))

    out = capsys.readouterr().out
    assert "converted  a_reencode.avi" in out
    assert "remuxed    b_remux.mkv" in out
    assert "2 converted, 1 remuxed, 0 skipped, 0 failed" in out


def test_rerun_is_noop(folder: Path, capsys):
    to_mp4.run(folder)
    before = {p.name: p.stat().st_mtime_ns for p in folder.iterdir()}
    capsys.readouterr()

    assert to_mp4.run(folder) == 0

    assert {p.name: p.stat().st_mtime_ns for p in folder.iterdir()} == before
    assert "0 converted, 0 remuxed, 3 skipped, 0 failed" in capsys.readouterr().out


def test_skips_uppercase_existing_target(tmp_path: Path):
    make_video(tmp_path / "clip.avi", "mpeg4", None)
    (tmp_path / "clip.MP4").write_bytes(b"placeholder")

    assert to_mp4.run(tmp_path) == 0
    assert (tmp_path / "clip.MP4").read_bytes() == b"placeholder"


def test_removes_leftover_partial_files(tmp_path: Path):
    (tmp_path / "old.mp4.partial").write_bytes(b"junk")

    to_mp4.run(tmp_path)

    assert not (tmp_path / "old.mp4.partial").exists()


def test_failure_writes_log_and_continues(folder: Path, monkeypatch, capsys):
    real = to_mp4.codec_args

    def broken(info, video):
        kind, args = real(info, video)
        return kind, ["-c:v", "no_such_codec"] if kind == "converted" else args

    monkeypatch.setattr(to_mp4, "codec_args", broken)

    assert to_mp4.run(folder) == 1

    log = folder / "a_reencode.error.log"
    assert "no_such_codec" in log.read_text(encoding="utf-8")
    assert not (folder / "a_reencode.mp4").exists()
    assert (folder / "b_remux.mp4").exists()
    assert not list(folder.glob("*.partial"))
    assert "1 remuxed, 0 skipped, 2 failed" in capsys.readouterr().out


def test_success_removes_stale_error_log(folder: Path):
    (folder / "a_reencode.error.log").write_text("old failure")

    assert to_mp4.run(folder) == 0

    assert not (folder / "a_reencode.error.log").exists()


def test_every_file_ends_as_mp4_or_error_log(tmp_path: Path, capsys):
    make_video(tmp_path / "clip.avi", "mpeg4", None)
    (tmp_path / "broken.mkv").write_bytes(b"\x00\x01garbage" * 50)
    (tmp_path / "notes.txt").write_text("not a video")
    ffmpeg("-f", "lavfi", "-i", "color=red:size=8x8", "-frames:v", "1", str(tmp_path / "picture.png"))
    ffmpeg("-f", "lavfi", "-i", "sine=duration=1", str(tmp_path / "song.mp3"))

    assert to_mp4.run(tmp_path) == 1

    assert (tmp_path / "clip.mp4").exists()
    for stem in ("broken", "notes", "picture", "song"):
        assert not (tmp_path / f"{stem}.mp4").exists()
        assert (tmp_path / f"{stem}.error.log").read_text(encoding="utf-8").strip()
    assert "ffprobe could not read" in (tmp_path / "broken.error.log").read_text(encoding="utf-8")
    assert "Not a video" in (tmp_path / "song.error.log").read_text(encoding="utf-8")
    assert "1 converted, 0 remuxed, 0 skipped, 4 failed" in capsys.readouterr().out


def test_error_logs_are_not_processed_on_rerun(tmp_path: Path, capsys):
    (tmp_path / "notes.txt").write_text("not a video")
    to_mp4.run(tmp_path)
    capsys.readouterr()

    assert to_mp4.run(tmp_path) == 1

    assert sorted(p.name for p in tmp_path.iterdir()) == ["notes.error.log", "notes.txt"]
    assert "0 skipped, 1 failed" in capsys.readouterr().out


def test_missing_folder(tmp_path: Path):
    assert to_mp4.run(tmp_path / "nope") == 2
