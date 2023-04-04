
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

"""

metainfo files
--------------
Metainfo files (also known as .torrent files) are bencoded dictionaries with the following keys:

announce
--------
The URL of the tracker.
info
This maps to a dictionary, with keys described below.
All strings in a .torrent file that contains text must be UTF-8 encoded.

info dictionary
---------------
The name key maps to a UTF-8 encoded string which is the suggested name to save the file (or directory) as. It is purely advisory.
piece length maps to the number of bytes in each piece the file is split into. For the purposes of transfer, files are split into fixed-size pieces which are all the same length except for possibly the last one which may be truncated. piece length is almost always a power of two, most commonly 2 18 = 256 K (BitTorrent prior to version 3.2 uses 2 20 = 1 M as default).
pieces maps to a string whose length is a multiple of 20. It is to be subdivided into strings of length 20, each of which is the SHA1 hash of the piece at the corresponding index.
There is also a key length or a key files, but not both or neither. If length is present then the download represents a single file, otherwise it represents a set of files which go in a directory structure.
In the single file case, length maps to the length of the file in bytes.
For the purposes of the other keys, the multi-file case is treated as only having a single file by concatenating the files in the order they appear in the files list. The files list is the value files maps to, and is a list of dictionaries containing the following keys:
length - The length of the file, in bytes
path - A list of UTF-8 encoded strings corresponding to subdirectory names, the last of which is the actual file name (a zero length list is an error case).
In the single file case, the name key is the name of a file, in the muliple file case, it's the name of a directory.

Text credit: https://wiki.theory.org/BitTorrentSpecification#Metainfo_File_Structure
"""

from app.repositories.bt_file import BTFile, BTFileCollection

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
        # Initialize TorrentInfo object with name, size of each piece, list of piece hashes, 
        # total length of the torrent (optional), list of FileInfo objects (optional), 
        # and whether the torrent is private (optional)
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
        # Initialize TorrentFile object with the path and length of the file
        self.path = path
        self.length = length

    def __str__(self):
        return f"TorrentFile(path={self.path}, length={self.length})"