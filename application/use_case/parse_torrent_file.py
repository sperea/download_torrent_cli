import urllib.parse
from application.infra.torrent_source_file import TorrentInfo, Torrent, TorrentFile, Tracker, FileInfo


class BencodeDecoder:
    def __init__(self, data, index=0):
        self.data = data
        self.index = index

    def decode(self):
        if self.data[self.index] == ord(b'd'):
            return self.decode_dictionary()
        elif self.data[self.index] == ord(b'l'):
            return self.decode_list()
        elif self.data[self.index] == ord(b'i'):
            return self.decode_integer()
        else:
            return self.decode_string()

    def decode_dictionary(self):
        dct = {}
        self.index += 1
        while self.data[self.index] != ord(b'e'):
            key = self.decode_string()
            value = self.decode()
            dct[key.decode()] = value
        self.index += 1
        return dct

    def decode_list(self):
        lst = []
        self.index += 1
        while self.data[self.index] != ord(b'e'):
            item = self.decode()
            lst.append(item)
        self.index += 1
        return lst

    def decode_integer(self):
        end = self.data.index(b'e', self.index)
        integer = int(self.data[self.index + 1:end])
        self.index = end + 1
        return integer

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


class ParseTorrentFile:
    def __init__(self, file_path):
        self.file_path = file_path

    def execute(self):
        with open(self.file_path, "rb") as file:
            data = file.read()

        decoder = BencodeDecoder(data)
        torrent_dict = decoder.decode()

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

        torrent_info = TorrentInfo(
            name=info_dict["name"].decode(),
            piece_length=info_dict["piece length"],
            pieces=info_dict["pieces"],
            length=info_dict.get("length"),
            files=files if files else None,
            private=info_dict.get("private"),
        )

        torrent = Torrent(
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