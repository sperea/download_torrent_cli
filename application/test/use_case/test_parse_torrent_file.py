import unittest
import os
from application.use_case.parse_torrent_file import BencodeDecoder, ParseTorrentFile


class TestBencodeDecoder(unittest.TestCase):
    def decode_integer(self):
        end = self.data.index(b'e', self.index)
        integer = int(self.data[self.index + 1:end])
        next_char = chr(self.data[end + 1])
        if next_char.isdigit():
            self.index = end + 1
            return integer
        elif next_char == 'l':
            self.index = end + 1
            return self.decode_list()
        else:
            raise ValueError("Invalid data format: expected integer or list")

    def test_decode_string(self):
        decoder = BencodeDecoder(b"5:hello")
        result = decoder.decode()
        self.assertEqual(result, b"hello")

    def test_decode_list(self):
        decoder = BencodeDecoder(b"l5:helloi42ee")
        result = decoder.decode()
        self.assertEqual(result, [b"hello", 42])

    def test_decode_dictionary(self):
        decoder = BencodeDecoder(b"d3:key5:valuee")
        result = decoder.decode()
        self.assertEqual(result, {"key": b"value"})

class TestParseTorrentFile(unittest.TestCase):

    def setUp(self):
        self.test_torrent_file = os.path.join(os.path.dirname(__file__), 'files', 'linuxiso.torrent')

    def test_parse_torrent_file(self):
        parser = ParseTorrentFile(self.test_torrent_file )
        torrent = parser.execute()
        self.assertEqual(torrent.info.piece_length, 262144)
        self.assertEqual(torrent.files, None)