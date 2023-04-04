
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

from application.infra.bt_file import BTFile, BTFileCollection

# Define the MetaInfo class to store torrent metadata
class MetaInfo:
    def __init__(self, announce, info, announce_list=None, comment=None, created_by=None, creation_date=None, encoding=None, files=None):
        self.announce = announce # The main tracker URL
        self.announce_list = announce_list # List of alternative tracker URLs
        self.comment = comment # Optional comment from the torrent creator
        self.created_by = created_by # Name of the torrent creator
        self.creation_date = creation_date # Timestamp when the torrent was created
        self.encoding = encoding # Encoding used for the torrent
        self.info = info # TorrentInfo object containing information about the torrent
        self.files = files # List of FileInfo objects, one for each file in the torrent

    def create_btfile_collection(self):
        btfile_collection = BTFileCollection()
        current_byte = 0

        if self.files is None:
            # The torrent is a single file
            if self.info.length < 0:
                raise ValueError("Invalid file length")
            bt_file = BTFile(self.info.name, self.info.length, 0, self.info.length - 1)
            btfile_collection.add_file(bt_file)
        else:
            # The torrent contains multiple files
            for file_info in self.files:
                bt_file = BTFile(file_info.path, file_info.length, current_byte, current_byte + file_info.length - 1)
                btfile_collection.add_file(bt_file)
                current_byte += file_info.length

        return btfile_collection

# Define the FileInfo class to store information about individual files in a torrent
class FileInfo:
    def __init__(self, length, md5sum, path):
        self.length = length
        self.md5sum = md5sum
        self.path = path


class Tracker:
    def __init__(self, url):
        self.url = url

class TorrentInfo:
    def __init__(self, name, piece_length, pieces, length=None, files=None, private=None):
        self.name = name
        self.piece_length = piece_length
        self.pieces = pieces
        self.length = length
        self.files = files
        self.private = private

    def __str__(self):
        return f"TorrentInfo(name={self.name}, piece_length={self.piece_length}, pieces={len(self.pieces)}, length={self.length}, files={self.files}, private={self.private})"


class TorrentFile:
    def __init__(self, path, length):
        self.path = path
        self.length = length

    def __str__(self):
        return f"TorrentFile(path={self.path}, length={self.length})"