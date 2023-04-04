


"""
This code defines two classes: BTFile and BTFileCollection. The purpose of this code is to manage the reading and writing of files in a torrent file collection, as well as to compute SHA-1 hashes for data verification. This is particularly useful in applications that work with torrent files, such as torrent download clients.
"""

import os
import hashlib

class BTFile:
    """
    The BTFile class represents an individual file within a torrent file and has the following properties:
    - path: The file path in the file system.
    - size: The file size in bytes.
    - start_byte: The starting byte in the torrent byte range.
    - end_byte: The ending byte in the torrent byte range.
    """
    def __init__(self, path, size, start_byte, end_byte):
        self.path = path
        self.size = size
        self.start_byte = start_byte
        self.end_byte = end_byte


class BTFileCollection:
    """
    The BTFileCollection class represents a collection of BTFile objects and has the following functions:
        - add_file: Adds a BTFile object to the collection.
        - get_files: Returns the list of BTFile objects in the collection.
        - read_offset: Reads a specific amount of bytes (amount) from a specific position (offset) in the files of the collection. Returns the read data as a bytearray object.
        - write_offset: Writes data at a specific position (offset) in the files of the collection. The data is written at the specified position across all appropriate files in the collection.
        - all_sha1_split_every: Computes and returns a list of SHA-1 hashes for each piece_length-byte block of data across all files in the collection. This is useful for data integrity verification in torrent download applications.
        - total_size: Returns the total size in bytes of all files in the collection.
    """
    def __init__(self, files=None):
        self.files = files or []

    def add_file(self, bt_file):
        self.files.append(bt_file)

    def get_files(self):
        return self.files

    def read_offset(self, offset, amount, output_directory):
        data = bytearray()
        current_offset = 0

        for bt_file in self.get_files():
            if (bt_file.start_byte <= offset <= bt_file.end_byte) or (bt_file.start_byte <= offset + amount - 1 <= bt_file.end_byte):
                file_start = max(0, offset - current_offset)
                file_end = min(bt_file.end_byte + 1, offset + amount - current_offset)

                with open(os.path.join(output_directory, bt_file.path), 'rb') as f:
                    f.seek(file_start)
                    file_data = f.read(file_end - file_start)
                    data.extend(file_data)

            current_offset += bt_file.size

        return data

    def write_offset(self, offset, data, output_directory):
        remaining_data = data
        current_offset = 0

        for bt_file in self.get_files():
            if (bt_file.start_byte <= offset <= bt_file.end_byte) or (bt_file.start_byte <= offset + len(data) - 1 <= bt_file.end_byte):
                file_start = max(0, offset - current_offset)
                file_end = min(bt_file.end_byte + 1, offset + len(data) - current_offset)

                with open(os.path.join(output_directory, bt_file.path), 'rb+') as f:
                    f.seek(file_start)
                    f.write(remaining_data[:file_end - file_start])
                    f.flush()
                    remaining_data = remaining_data[file_end - file_start:]

                if not remaining_data:
                    break

            current_offset += bt_file.size

    def all_sha1_split_every(self, piece_length, output_directory):
        current_offset = 0
        sha1_list = []

        while current_offset < self.total_size():
            data = self.read_offset(current_offset, piece_length, output_directory)
            sha1_hash = hashlib.sha1(data).digest()
            sha1_list.append(sha1_hash)
            current_offset += piece_length

        return sha1_list

    def total_size(self):
        return sum(file.size for file in self.files)