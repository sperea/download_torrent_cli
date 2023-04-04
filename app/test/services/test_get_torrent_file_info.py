import unittest
from unittest.mock import Mock
from app.services.torrent_file_info import TorrentInfo


class TestTorrentInfo(unittest.TestCase):

    def setUp(self):
        self.mock_torrent_file = Mock()
        self.mock_torrent_file.announce = "http://test.com"
        self.mock_torrent_file.comment = "This is a test torrent"
        self.mock_torrent_file.created_by = "Test Client"
        self.mock_torrent_file.creation_date = "2022-05-12 15:24:35"
        self.mock_torrent_file.encoding = "UTF-8"

        self.mock_file1 = Mock()
        self.mock_file1.path = "test_file_1.txt"
        self.mock_file1.length = 1024

        self.mock_file2 = Mock()
        self.mock_file2.path = "test_file_2.txt"
        self.mock_file2.length = 2048

        self.mock_torrent_file.files = [self.mock_file1, self.mock_file2]

        self.mock_torrent_file.announce_list = []
        self.mock_torrent_file.files = []

    def test_torrent_info_str(self):
        torrent_info = TorrentInfo(self.mock_torrent_file)
        assert str(torrent_info).startswith("=== TORRENT INFO ===")
        assert str(torrent_info).endswith("=== END TORRENT INFO ===\n")

    def test_torrent_info_str_with_no_files(self):
        torrent_info = TorrentInfo(self.mock_torrent_file)
        assert str(torrent_info).startswith("=== TORRENT INFO ===")
        assert str(torrent_info).endswith("=== END TORRENT INFO ===\n")