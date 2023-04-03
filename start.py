import os
import sys
import argparse

from application.services.torrent_file_info import TorrentInfo
from application.use_case.parse_torrent_file import ParseTorrentFile


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Cli Torrent Downloader. version 1.0. Run: %(prog)s. Written by Sergio Perea (https://sperea.es)")
    parser.add_argument("--t", type=str, default="media",
                        help="Torrent file download. Specifies the path of the torrent file")
    parser.add_argument("--v", action='version', version='%(prog)s 1.0')
    parser.add_argument("--h", action='help', help="Show available options")

    return parser.parse_args()


def main(args):
    script_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    torrent_file = os.path.join(script_path, args.t)

    if os.path.exists(torrent_file):
        print("Running with the following parameters:")
        print(f"Torrent file: {args.t}")

        torrent = ParseTorrentFile(torrent_file).execute()
        print(str(TorrentInfo(torrent)))

        bt_files = torrent.create_btfile_collection()
        print(str(bt_files))

    else:
        print("No torrent file found.")


if __name__ == "__main__":
    args = parse_arguments()
    main(args)