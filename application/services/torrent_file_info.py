import unittest

class TorrentInfo:
    def __init__(self, torrent_file):
        self.torrent_file = torrent_file
        self.info = ""
        self.info += "=== TORRENT INFO ===\n"
        self.info += f"Announce: {self.torrent_file.announce}\n"
        if self.torrent_file.announce_list:
            self.info += "Announce list:\n"
            for tracker in self.torrent_file.announce_list:
                self.info += f"  - {tracker.url}\n"
        if self.torrent_file.comment:
            self.info += f"Comment: {self.torrent_file.comment}\n"
        if self.torrent_file.created_by:
            self.info += f"Created by: {self.torrent_file.created_by}\n"
        if self.torrent_file.creation_date:
            self.info += f"Creation date: {self.torrent_file.creation_date}\n"
        if self.torrent_file.encoding:
            self.info += f"Encoding: {self.torrent_file.encoding}\n"
        self.info += "=== FILE INFO ===\n"
        if self.torrent_file.files:
            self.info += f"Files:\n"
            for file in self.torrent_file.files:
                self.info += f" ---> {file.path} ({file.length} bytes)\n"
        else:
            self.info += f"{self.torrent_file.info.name} ({self.torrent_file.info.length} bytes)\n"
        self.info += "=== END TORRENT INFO ===\n"

    def __str__(self):
        return self.info