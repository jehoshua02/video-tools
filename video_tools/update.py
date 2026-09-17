import shutil
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def run() -> int:
    if not shutil.which("git"):
        print("error: git not found on PATH. Run install.ps1.")
        return 2
    if not (REPO / ".git").exists():
        print(f"error: {REPO} is not a git clone, so it can't update itself. Reinstall with the one-liner in the README.")
        return 2
    print(f"Updating {REPO}...", flush=True)
    return subprocess.run(["git", "-C", str(REPO), "pull", "--ff-only"]).returncode
