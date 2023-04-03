

class TorrentInfoPrinter:
    def __init__(self, torrent_file):
        self.torrent_file = torrent_file

    def execute(self):
        print("=== TORRENT INFO ===")
        print(f"Announce: {self.torrent_file.announce}")
        if self.torrent_file.announce_list:
            print("Announce list:")
            for tracker in self.torrent_file.announce_list:
                print(f"  - {tracker.url}")
        if self.torrent_file.comment:
            print(f"Comment: {self.torrent_file.comment}")
        if self.torrent_file.created_by:
            print(f"Created by: {self.torrent_file.created_by}")
        if self.torrent_file.creation_date:
            print(f"Creation date: {self.torrent_file.creation_date}")
        if self.torrent_file.encoding:
            print(f"Encoding: {self.torrent_file.encoding}")
        #Info: {torrent_file.info}")
        print("=== FILE INFO ===")
        if self.torrent_file.files:
            print(f"Files:")
            for file in self.torrent_file.files:
                print(f" ---> {file.path} ({file.length} bytes)")
        else:
            print(f"{self.torrent_file.info.name} ({self.torrent_file.info.length} bytes)")