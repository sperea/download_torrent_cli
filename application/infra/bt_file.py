import os

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

    def get_file(self, index):
        return self.files[index]

    def get_files(self):
        return self.files

    def read(self, start_byte, length, output_directory):
        data = bytearray()
        for bt_file in self.files:
            if bt_file.end_byte < start_byte or bt_file.start_byte > start_byte + length:
                continue

            file_start = max(0, start_byte - bt_file.start_byte)
            file_end = min(bt_file.size, start_byte + length - bt_file.start_byte)

            with open(os.path.join(output_directory, bt_file.path), 'rb') as f:
                f.seek(file_start)
                file_data = f.read(file_end - file_start)
                data.extend(file_data)

        return data

    def write(self, start_byte, data, output_directory):
        remaining_data = data
        for bt_file in self.files:
            if bt_file.end_byte < start_byte or bt_file.start_byte > start_byte + len(data):
                continue

            file_start = max(0, start_byte - bt_file.start_byte)
            file_end = min(bt_file.size, start_byte + len(data) - bt_file.start_byte)

            with open(os.path.join(output_directory, bt_file.path), 'rb+') as f:
                f.seek(file_start)
                f.write(remaining_data[:file_end - file_start])
                remaining_data = remaining_data[file_end - file_start:]