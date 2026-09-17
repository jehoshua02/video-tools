# 0001. Use Python as the CLI runtime

## Status
Accepted

## Context
video-tools is a new command-line video toolkit. Need a language with strong
scripting ergonomics, batch/file-processing libraries, and low ceremony for a
solo-maintained CLI.

## Decision
Build the CLI in Python.

## Consequences
- Distribution via pip; users need a Python environment.
- Rich stdlib (pathlib, argparse) plus ecosystem (watchdog, click/typer) available.
- No single static binary; startup slightly slower than Go/Rust alternatives.
