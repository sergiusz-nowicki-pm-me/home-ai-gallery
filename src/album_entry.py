import os
from src.json_file import JsonFile


GENERIC_ENTRY = 'GENERIC'


class AlbumEntry:
    def __init__(self, file_path):
        self.file_path = file_path
        self.metadata_file = JsonFile(os.path.basename(file_path))
        
        
    def __load_metadata(self):
        metadata = JsonFile.load()
        if self.file_path in metadata:
            pass


    def get_name(self):
        return os.path.basename(self.file_path)


    def is_generic(self):
        pass


    # def get_preview(self):
    #     return f'<img src="/image-preview/{self.file_path}" style="height:{self.config["preview_size"]}px; width:auto;" />'


    def get_image(self):
        return f'<img src="/image/{self.file_path}" />'