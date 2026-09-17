import subprocess
from pathlib import Path

import pytest

from video_tools import cli, download

URL = "https://www.youtube.com/watch?v=example"


@pytest.fixture
def calls(monkeypatch):
    recorded = []

    def fake_run(cmd, *args, **kwargs):
        recorded.append(cmd)
        return subprocess.CompletedProcess(cmd, 0)

    monkeypatch.setattr(download.shutil, "which", lambda name: name)
    monkeypatch.setattr(download.subprocess, "run", fake_run)
    return recorded


def test_downloads_to_given_folder(tmp_path: Path, calls):
    assert cli.main(["download", URL, "-o", str(tmp_path)]) == 0

    assert calls == [[
        "yt-dlp", "--no-playlist",
        "-f", "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]",
        "--merge-output-format", "mp4",
        "-o", str(tmp_path / "%(title)s.%(ext)s"),
        URL,
    ]]


def test_defaults_to_downloads_folder(tmp_path: Path, calls, monkeypatch):
    (tmp_path / "Downloads").mkdir()
    monkeypatch.setattr(download.Path, "home", lambda: tmp_path)

    assert download.run(URL) == 0

    assert calls[0][-2] == str(tmp_path / "Downloads" / "%(title)s.%(ext)s")


def test_passes_through_yt_dlp_exit_code(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(download.shutil, "which", lambda name: name)
    monkeypatch.setattr(download.subprocess, "run", lambda cmd: subprocess.CompletedProcess(cmd, 1))

    assert download.run(URL, tmp_path) == 1


def test_missing_folder(tmp_path: Path, calls):
    assert download.run(URL, tmp_path / "nope") == 2
    assert calls == []


def test_missing_yt_dlp(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.setattr(download.shutil, "which", lambda name: None if name == "yt-dlp" else name)

    assert download.run(URL, tmp_path) == 2
    assert "yt-dlp not found" in capsys.readouterr().out
