import subprocess
from pathlib import Path

from video_tools import cli, update


def test_pulls_the_install_folder(tmp_path: Path, monkeypatch, capsys):
    (tmp_path / ".git").mkdir()
    calls = []
    monkeypatch.setattr(update, "REPO", tmp_path)
    monkeypatch.setattr(update.shutil, "which", lambda name: name)
    monkeypatch.setattr(update.subprocess, "run", lambda cmd: calls.append(cmd) or subprocess.CompletedProcess(cmd, 0))

    assert cli.main(["update"]) == 0

    assert calls == [["git", "-C", str(tmp_path), "pull", "--ff-only"]]


def test_passes_through_git_exit_code(tmp_path: Path, monkeypatch):
    (tmp_path / ".git").mkdir()
    monkeypatch.setattr(update, "REPO", tmp_path)
    monkeypatch.setattr(update.shutil, "which", lambda name: name)
    monkeypatch.setattr(update.subprocess, "run", lambda cmd: subprocess.CompletedProcess(cmd, 1))

    assert update.run() == 1


def test_not_a_git_clone(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.setattr(update, "REPO", tmp_path)
    monkeypatch.setattr(update.shutil, "which", lambda name: name)

    assert update.run() == 2
    assert "not a git clone" in capsys.readouterr().out


def test_repo_points_at_this_checkout():
    assert (update.REPO / "video_tools" / "update.py").exists()
