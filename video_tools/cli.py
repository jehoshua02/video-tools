import argparse
from pathlib import Path

from video_tools import to_mp4


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m video_tools")
    commands = parser.add_subparsers(dest="command", required=True)

    p = commands.add_parser("to-mp4", help="convert every video in a folder to mp4")
    p.add_argument("folder", type=Path)

    args = parser.parse_args(argv)
    if args.command == "to-mp4":
        return to_mp4.run(args.folder)
    return 2
