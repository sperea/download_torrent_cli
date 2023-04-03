

class GenerateBtFileCollection:
    def __init__(self, meta_info):
        self.meta_info = meta_info

    def execute(self):
        return self.meta_info.create_btfile_collection()