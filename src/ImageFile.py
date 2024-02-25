import os


class ImageFile:
    def __init__(self, file_path, base_dir_path, config):
        self.file_path = file_path
        self.base_dir_path = base_dir_path
        self.config = config

    
    def get_name(self):
        return os.path.basename(self.file_path)
    

    def get_preview(self):
        return f'<img src="/image-preview/{self.file_path}" style="height:{self.config["preview_size"]}px; width:auto;" />'


    def get_image(self):
        return f'<img src="/image/{self.file_path}" />'