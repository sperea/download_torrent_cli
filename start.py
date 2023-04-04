
"""
Copyright (C) 2023 Sergio Perea

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Author: Sergio Perea
Website: https://sperea.es

Please give credit to the author and the website when using or redistributing this code.
"""

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