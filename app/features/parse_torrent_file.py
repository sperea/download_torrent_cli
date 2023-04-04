
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
bencoding
---------

Strings are length-prefixed base ten followed by a colon and the string. For example 4:spam corresponds to 'spam'.

Integers are represented by an 'i' followed by the number in base 10 followed by an 'e'. 
For example i3e corresponds to 3 and i-3e corresponds to -3. 

Integers have no size limitation. i-0e is invalid. 

All encodings with a leading zero, such as i03e, are invalid, other than i0e, which of course corresponds to 0.

Lists are encoded as an 'l' followed by their elements (also bencoded) followed by an 'e'. 
For example l4:spam4:eggse corresponds to ['spam', 'eggs'].

Dictionaries are encoded as a 'd' followed by a list of alternating keys and their corresponding values followed by an 'e'. 
For example, d3:cow3:moo4:spam4:eggse corresponds to {'cow': 'moo', 'spam': 'eggs'} and d4:spaml1:a1:bee corresponds to {'spam': ['a', 'b']}. 

Keys must be strings and appear in sorted order (sorted as raw strings, not alphanumerics).

For more information on the BitTorrent protocol, 
please refer to the [official BitTorrent specification](https://www.bittorrent.org/beps/bep_0003.html).
"""

import urllib.parse
from app.repositories.meta_info import TorrentInfo, MetaInfo, TorrentFile, Tracker, FileInfo

# BencodeDecoder class is responsible for decoding bencoded data.
class BencodeDecoder:
    def __init__(self, data, index=0):
        self.data = data
        self.index = index

    # The decode method determines the appropriate decoding method to use.
    def decode(self):
        if self.data[self.index] == ord(b'd'):
            return self.decode_dictionary()
        elif self.data[self.index] == ord(b'l'):
            return self.decode_list()
        elif self.data[self.index] == ord(b'i'):
            return self.decode_integer()
        else:
            return self.decode_string()

    # Decodes a bencoded dictionary.
    def decode_dictionary(self):
        dct = {}
        self.index += 1
        while self.data[self.index] != ord(b'e'):
            key = self.decode_string()
            value = self.decode()
            dct[key.decode()] = value
        self.index += 1
        return dct

    # Decodes a bencoded list.
    def decode_list(self):
        lst = []
        self.index += 1
        while self.data[self.index] != ord(b'e'):
            item = self.decode()
            lst.append(item)
        self.index += 1
        return lst

    # Decodes a bencoded integer.
    def decode_integer(self):
        end = self.data.index(b'e', self.index)
        integer = int(self.data[self.index + 1:end])
        self.index = end + 1
        return integer

    # Decodes a bencoded string.
    def decode_string(self):
        start = self.index
        while chr(self.data[self.index]).isdigit():
            self.index += 1
        colon = self.data.index(b':', self.index)
        length = int(self.data[start:colon].decode())
        end = colon + 1 + length
        string = self.data[colon + 1:end]
        self.index = end
        return string

# ParseTorrentFile class parses a torrent file and extracts relevant information.
class ParseTorrentFile:
    def __init__(self, file_path):
        self.file_path = file_path

    def execute(self):
        # Read the torrent file.
        with open(self.file_path, "rb") as file:
            data = file.read()

        # Decode the bencoded data.
        decoder = BencodeDecoder(data)
        torrent_dict = decoder.decode()

        # Extract information from the torrent dictionary.
        info_dict = torrent_dict["info"]
        files = []
        if "files" in info_dict:
            for file_info in info_dict["files"]:
                file_path = "/".join([path.decode() for path in file_info["path"]])
                file_length = file_info["length"]
                files.append(TorrentFile(file_path, file_length))

        announce_list = []
        if "announce-list" in torrent_dict:
            for announce_group in torrent_dict["announce-list"]:
                for announce_url in announce_group:
                    announce_list.append(Tracker(announce_url.decode()))

        # Create TorrentInfo object.
        torrent_info = TorrentInfo(
            name=info_dict["name"].decode(),
            piece_length=info_dict["piece length"],
            pieces=info_dict["pieces"],
            length=info_dict.get("length"),
            files=files if files else None,
            private=info_dict.get("private"),
        )

        # Create MetaInfo object.
        torrent = MetaInfo(
            announce=Tracker(torrent_dict["announce"].decode()),
            announce_list=announce_list,
            comment=torrent_dict.get("comment"),
            created_by=torrent_dict.get("created by"),
            creation_date=torrent_dict.get("creation date"),
            encoding=torrent_dict.get("encoding"),
            info=torrent_info,
            files=files if files else None,
        )

        return torrent