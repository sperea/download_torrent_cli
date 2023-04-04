
import unittest
from app.repositories.bt_file import BTFile, BTFileCollection
import pytest
from unittest.mock import Mock
from datetime import datetime
from app.repositories.meta_info import MetaInfo, TorrentInfo, TorrentFile, Tracker
from app.repositories.meta_info import TorrentInfo
from app.repositories.meta_info import MetaInfo
from app.repositories.meta_info import TorrentFile
from app.repositories.meta_info import Tracker


class TestTorrent(unittest.TestCase):
    """

    """
    def setUp(self):
        self.tracker1 = Tracker("http://tracker1.example.com/announce")
        self.tracker2 = Tracker("http://tracker2.example.com/announce")
        file1 = TorrentFile("folder1/file1.txt", 1000)
        file2 = TorrentFile("folder2/file2.txt", 2000)
        self.torrent_info = TorrentInfo("Test Torrent", 1024, b"abcd" * 20, length=3000, files=[file1, file2])
        files = [file1, file2 ]
        self.torrent = MetaInfo("http://example.com/announce", self.torrent_info, announce_list=[self.tracker1, self.tracker2], comment="Test Comment", created_by="Test Creator", creation_date=datetime.now(), encoding="UTF-8", files=files)


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



def test_create_btfile_collection_single_file(mocker):
    # Setup
    info = mocker.Mock()
    info.name = "test_file.txt"
    info.length = 100
    meta_info = MetaInfo("test_announce", info)

    # Execution
    btfile_collection = meta_info.create_btfile_collection()

    # Assertion
    assert len(btfile_collection.get_files()) == 1
    assert btfile_collection.get_files()[0].path == "test_file.txt"
    assert btfile_collection.get_files()[0].size == 100



# Tests that the create_btfile_collection method returns a btfilecollection object with the correct number of btfile objects when the torrent file contains multiple files. tags: [happy path]
def test_create_btfile_collection_multiple_files(mocker):
    # Setup
    file_info_1 = mocker.Mock()
    file_info_1.path = "test_file_1.txt"
    file_info_1.length = 100
    file_info_2 = mocker.Mock()
    file_info_2.path = "test_file_2.txt"
    file_info_2.length = 200
    info = mocker.Mock()
    info.name = "test_torrent"
    info.length = 300
    meta_info = MetaInfo("test_announce", info, files=[file_info_1, file_info_2])

    # Execution
    btfile_collection = meta_info.create_btfile_collection()

    # Assertion
    assert len(btfile_collection.get_files()) == 2
    assert btfile_collection.get_files()[0].path == "test_file_1.txt"
    assert btfile_collection.get_files()[0].size == 100
    assert btfile_collection.get_files()[1].path == "test_file_2.txt"
    assert btfile_collection.get_files()[1].size == 200


# Tests that the create_btfile_collection method raises an exception when the torrent file contains invalid or missing file information. tags: [edge case]
def test_create_btfile_collection_invalid_file_info(mocker):
    # Setup
    info = mocker.Mock()
    info.files = None
    info.name = "test_torrent"
    info.length = -300  # Set an invalid length
    meta_info = MetaInfo("test_announce", info)

    # Assertion
    with pytest.raises(ValueError): 
        meta_info.create_btfile_collection()


# Tests that an exception is raised when creating a metainfo object with missing required metadata fields. tags: [edge case]
def test_create_btfile_collection_missing_required_metadata():
    with pytest.raises(Exception):
        meta_info = MetaInfo(announce="http://example.com", info={})
        meta_info.create_btfile_collection()

# Tests that an exception is raised when creating a metainfo object with invalid metadata fields. tags: [edge case]
def test_create_btfile_collection_invalid_metadata():
    with pytest.raises(Exception):
        meta_info = MetaInfo(announce="http://example.com", info={"name": "test", "length": "invalid"})
        meta_info.create_btfile_collection()


# Tests that the all_sha1_split_every method of the btfilecollection class returns a list of sha-1 hashes for each piece_length-byte block of data across all files in the collection. tags: [behavior]
def test_all_sha1_split_every(mocker):
    # Create mock BTFile objects
    bt_file_1 = BTFile("file1.txt", 100, 0, 99)
    bt_file_2 = BTFile("file2.txt", 200, 100, 299)

    # Create mock BTFileCollection object
    bt_file_collection = BTFileCollection([bt_file_1, bt_file_2])

    # Mock read_offset method to return mock data
    mocker.patch.object(bt_file_collection, "read_offset", return_value=bytearray(b"test data"))

    # Test all_sha1_split_every method
    sha1_list = bt_file_collection.all_sha1_split_every(10, "output_dir")
    assert len(sha1_list) == 30

def test_write_offset(mocker):
    # Test that the write_offset method of the btfilecollection class correctly writes data at a specific position in the files of the collection and the data is written at the specified position across all appropriate files in the collection.
    bt_file1 = BTFile('test_file1', 100, 0, 99)
    bt_file2 = BTFile('test_file2', 200, 100, 299)
    btfile_collection = BTFileCollection([bt_file1, bt_file2])

    open_mock = mocker.mock_open()  # Assign the result of mocker.mock_open() to open_mock
    mocker.patch('builtins.open', open_mock)  # Patch builtins.open with the open_mock variable

    btfile_collection.write_offset(50, b'test_data', 'output_dir')
    
    open_mock().write.assert_called_once_with(b'test_data')