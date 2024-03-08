import copy
import hashlib
import os
from src.json_file import JsonFile


class Branches:
    def __init__(self):
        self.file = JsonFile('config/branches.json', default=[])


    def get_all(self):
        return self.file.get_data()


    def add(self, path):
        if len(path.strip()) == 0:
            return 'Empty path'
        
        clean_path = path.strip()
        md5 = hashlib.md5(clean_path.encode('utf-8')).hexdigest()
        paths = self.file.get_data()

        for item in paths:
            if md5 == item['md5']:
                return 'Duplicate branch path'

        if not os.path.exists(clean_path):
            return 'Path not found'

        paths.append({'md5': md5, 'path': clean_path})
        self.file.set_data(paths)

        return 'ok'
    

    def remove(self, md5):
        if len(md5) == 0:
            return 'Empty md5'
        
        paths = self.file.get_data()
        new_paths = []

        for item in paths:
            if md5 != item['md5']:
                new_paths.append(item)

        self.file.set_data(new_paths)

        return 'ok' 