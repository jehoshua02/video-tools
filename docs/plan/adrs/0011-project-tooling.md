# 0011. Project tooling: plain python, argparse, pytest

## Status
Accepted

## Context
Need a project setup for [[0001-python-runtime]] and [[0003-local-cli-distribution]].

## Decision
- Python 3.12+.
- Run with plain python: `python -m video_tools to-mp4 <folder>`. No uv.
- stdlib `argparse` for the CLI; no runtime dependencies.
- pytest for tests, installed in a venv via `pip` (dev-only). Integration tests generate tiny sample videos with ffmpeg.

## Consequences
- Running the tool needs only Python and ffmpeg; no install step.
- Only running tests needs a venv with pytest.
