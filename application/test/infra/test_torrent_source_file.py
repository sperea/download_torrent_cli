
import unittest
from datetime import datetime
from application.infra.torrent_source_file import Torrent, TorrentInfo, TorrentFile, Tracker

class TestTorrent(unittest.TestCase):
    def setUp(self):
        self.tracker1 = Tracker("http://tracker1.example.com/announce")
        self.tracker2 = Tracker("http://tracker2.example.com/announce")
        file1 = TorrentFile("folder1/file1.txt", 1000)
        file2 = TorrentFile("folder2/file2.txt", 2000)
        self.torrent_info = TorrentInfo("Test Torrent", 1024, b"abcd" * 20, length=3000, files=[file1, file2])
        files = [file1, file2 ]
        self.torrent = Torrent("http://example.com/announce", self.torrent_info, announce_list=[self.tracker1, self.tracker2], comment="Test Comment", created_by="Test Creator", creation_date=datetime.now(), encoding="UTF-8", files=files)


    def test_announce(self):
        self.assertEqual(self.torrent.announce, "http://example.com/announce")

    def test_announce_list(self):
        self.assertEqual(len(self.torrent.announce_list), 2)
        self.assertEqual(self.torrent.announce_list[0].url, "http://tracker1.example.com/announce")
        self.assertEqual(self.torrent.announce_list[1].url, "http://tracker2.example.com/announce")

    def test_comment(self):
        self.assertEqual(self.torrent.comment, "Test Comment")

    def test_created_by(self):
        self.assertEqual(self.torrent.created_by, "Test Creator")

    def test_creation_date(self):
        self.assertIsInstance(self.torrent.creation_date, datetime)

    def test_encoding(self):
        self.assertEqual(self.torrent.encoding, "UTF-8")

    def test_info(self):
        self.assertEqual(self.torrent.info.name, "Test Torrent")
        self.assertEqual(self.torrent.info.piece_length, 1024)
        self.assertEqual(self.torrent.info.pieces, b"abcd" * 20)
        self.assertEqual(self.torrent.info.length, 3000)
        self.assertEqual(len(self.torrent.info.files), 2)
        self.assertEqual(self.torrent.info.files[0].path, "folder1/file1.txt")
        self.assertEqual(self.torrent.info.files[0].length, 1000)
        self.assertEqual(self.torrent.info.files[1].path, "folder2/file2.txt")
        self.assertEqual(self.torrent.info.files[1].length, 2000)

    def test_files(self):
        self.assertEqual(len(self.torrent.files), 2)
        self.assertEqual(self.torrent.files[0].path, "folder1/file1.txt")
        self.assertEqual(self.torrent.files[0].length, 1000)
        self.assertEqual(self.torrent.files[1].path, "folder2/file2.txt")
        self.assertEqual(self.torrent.files[1].length, 2000)