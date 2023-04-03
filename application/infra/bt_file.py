import os
import hashlib

class BTFile:
    def __init__(self, path, size, start_byte, end_byte):
        self.path = path
        self.size = size
        self.start_byte = start_byte
        self.end_byte = end_byte


class BTFileCollection:
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
            if bt_file.start_byte <= current_offset + amount <= bt_file.end_byte:
                file_start = max(0, offset - current_offset)
                file_end = min(bt_file.end_byte, offset + amount - current_offset)

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
            if bt_file.start_byte <= current_offset + len(data) <= bt_file.end_byte:
                file_start = max(0, offset - current_offset)
                file_end = min(bt_file.end_byte, offset + len(data) - current_offset)

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