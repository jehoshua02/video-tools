# 0011. Project tooling: uv, argparse, pytest

## Status
Accepted

## Context
Need a project setup for [[0001-python-runtime]] and [[0003-local-cli-distribution]].

## Decision
- Python 3.12+.
- uv for environment, dependencies, and running (`uv run`).
- stdlib `argparse` for the CLI; no runtime dependencies.
- pytest for tests (dev dependency). Integration tests generate tiny sample videos with ffmpeg.

## Consequences
- Contributors need uv and ffmpeg installed.
- Zero runtime deps keeps install trivial.
