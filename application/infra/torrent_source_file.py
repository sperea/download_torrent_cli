class Torrent:
    def __init__(self, announce, info, announce_list=None, comment=None, created_by=None, creation_date=None, encoding=None, files=None):
        self.announce = announce
        self.announce_list = announce_list
        self.comment = comment
        self.created_by = created_by
        self.creation_date = creation_date
        self.encoding = encoding
        self.info = info
        self.files = files

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