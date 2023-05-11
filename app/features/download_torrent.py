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

import bencode
import requests
import time

class DownloadTorrentUseCase:

    def __init__(self, torrent_file, tracker_url):
        self.torrent_file = torrent_file
        self.tracker_url = tracker_url

    def download(self):
        # Get the info hash
        info_hash = get_info_hash(self.torrent_file)

        # Connect to the tracker
        announce_url = connect_to_tracker(info_hash, self.tracker_url)

        # Get the piece length
        piece_length = 256 * 1024

        # Download all the pieces
        for piece_index in range(len(info_hash)):
            download_piece(info_hash, piece_index, piece_length, announce_url)

        # Combine the pieces into a single file
        with open('output.torrent', 'wb') as f:
            for piece_index in range(len(info_hash)):
                with open('piece-%d' % piece_index, 'rb') as piece_file:
                    f.write(piece_file.read())

        print('The torrent has been downloaded.')