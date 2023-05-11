import unittest
import tempfile
import shutil
import os
from app.repositories.bt_file import BTFileCollection, BTFile
from base64 import encode, encodebytes
import os


torrent_file_mock = {
    'name': 'test.mp4',
    'piece length': 16384,
    'pieces': [
        '0123456789abcdef',
        'fedcba9876543210',
    ],
    'files': [
        {
            'length': 1024,
            'offset': 0,
        },
        {
            'length': 1024,
            'offset': 1024,
        },
    ],
}


class BTFileTest(unittest.TestCase):

    def test_init(self):
        with open('test.torrent', 'wb') as f:
            f.write(encodebytes.bencode(torrent_file_mock))

        bt_file = BTFile('test.torrent', 1024, 0, 1024)
        self.assertEqual(bt_file.path, 'test.torrent')
        self.assertEqual(bt_file.size, 1024)
        self.assertEqual(bt_file.start_byte, 0)
        self.assertEqual(bt_file.end_byte, 1023)

    def test_get_info_hash(self):
        with open('test.torrent', 'wb') as f:
            f.write(encodebytes.bencode(torrent_file_mock))

        bt_file = BTFile('test.torrent', 1024, 0, 1024)
        info_hash = bt_file.get_info_hash()
        self.assertEqual(info_hash, '0123456789abcdef')

class TestBTFileCollection(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

        self.files_data = {
            "file1.txt": b"Hello, World! This is file 1.",
            "file2.txt": b"Welcome to file 2.",
            "file3.txt": b"File 3 is the last file."
        }

        current_byte = 0
        self.btfile_collection = BTFileCollection()
        for filename, file_data in self.files_data.items():
            with open(os.path.join(self.test_dir, filename), "wb") as f:
                f.write(file_data)

            bt_file = BTFile(filename, len(file_data), current_byte, current_byte + len(file_data) - 1)
            self.btfile_collection.add_file(bt_file)
            current_byte += len(file_data)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_read(self):
        for bt_file in self.btfile_collection.get_files():
            data = self.btfile_collection.read_offset(bt_file.start_byte, bt_file.size, self.test_dir)
            self.assertEqual(data, self.files_data[bt_file.path])

    def test_write(self):
        new_data = b"modified"
        for bt_file in self.btfile_collection.get_files():
            self.btfile_collection.write_offset(bt_file.start_byte, new_data, self.test_dir)
            with open(os.path.join(self.test_dir, bt_file.path), "rb") as f:
                updated_data = f.read()
            self.assertEqual(updated_data[:len(new_data)], new_data)


