import argparse
from pathlib import Path

from video_tools import download, to_mp4, update


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="video-tools")
    commands = parser.add_subparsers(dest="command", required=True)

    p = commands.add_parser("to-mp4", help="convert every video in a folder to mp4")
    p.add_argument("folder", type=Path)

    p = commands.add_parser("download", help="download a YouTube video as mp4")
    p.add_argument("url")
    p.add_argument("-o", "--output", type=Path, help="folder to save into (default: ~\\Downloads)")

    commands.add_parser("update", help="update video-tools to the latest version")

    args = parser.parse_args(argv)
    if args.command == "to-mp4":
        return to_mp4.run(args.folder)
    if args.command == "download":
        return download.run(args.url, args.output)
    if args.command == "update":
        return update.run()
    return 2
