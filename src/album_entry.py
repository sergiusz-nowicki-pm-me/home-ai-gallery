import os
import hashlib
from PIL import Image
from src.json_file import JsonFile


GENERIC_ENTRY = 'GENERIC'
IMAGE_ENTRY = 'IMAGE'


class AlbumEntry:
    def __init__(self, file_path, metadata_json_file):
        print(f'Entry found {file_path}')
        if os.path.isfile(file_path):
            raise Exception("File path not exists!")

        self.file_path = file_path
        self.metadata_json_file = metadata_json_file

        local_metadata = self.metadata_json_file.get_data()
        if self.file_path not in local_metadata.keys():
            type = IMAGE_ENTRY
            try:
                with Image.open(self.file_path) as im:
                    im.load()
            except:
                type = GENERIC_ENTRY
            local_metadata[self.file_path] = {
                "digest": hashlib.md5(open(self.file_path,'rb').read()).hexdigest(),
                "type": type
            }
            self.metadata_json_file.set_data(local_metadata)
        
        
    def get_name(self):
        return os.path.basename(self.file_path)


    def get_path(self):
        return self.file_path


    def is_generic(self):
        return self.metadata_json_file.get_data()['type'] == GENERIC_ENTRY


    # def get_preview(self):
    #     return f'<img src="/image-preview/{self.file_path}" style="height:{self.config["preview_size"]}px; width:auto;" />'


    def get_image(self):
        return f'<img src="/image/{self.file_path}" />'
    

    def is_satisfying(self, search_condition):
        return True