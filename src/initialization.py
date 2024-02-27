import copy
import hashlib
import json
import os
import sqlite3
from PIL import Image
from src.ImageFile import ImageFile
from src.JsonFile import JsonFile

METADATA_FILE_NAME = '.home-ai-gallery-metadata'

        
class BaseDirectory:
    METADATA_FILE_NAME = '.home-ai-gallery-metadata'
    

    def __init__(self, path):
        self.path = path
        self.metadata_file_path = os.path.join(self.path, self.METADATA_FILE_NAME)
        self.json_file = JsonFile(self.metadata_file_path)
        
        self.metadata = self.json_file.load()


    def get_metadata(self):
        return copy.deepcopy(self.metadata)
    

    def get_files(self):
        all_files = []
        for root, dirs, files in os.walk(self.path):
            for file in files:
                file_path = os.path.join(root, file)
                if file != self.METADATA_FILE_NAME:
                    all_files.append(file_path)
        return all_files
    

    def get_files_without_metadata(self):
        metadata_keys = self.metadata.keys()
        return [path for path in self.get_files() if path not in metadata_keys]
    

    def get_path(self):
        return self.path
    

    def set_metadata(self, data):
        self.metadata = data
        self.json_file.save(data)

     

class Gallery:
    def __init__(self):
        self.metadata = {}
        self.base_directories = []
        self.config_file = JsonFile('config/conf.json', {"dirs": []})

        self.initialize()

        config = self.config_file.load()
        self.files = [ImageFile(m, self.metadata[m]['base_directory_path'], config) for m in self.metadata.keys() if self.metadata[m]['type'] == 'image']


    def initialize(self):        
        print('Loading configuration file')
        config = self.config_file.load()
        print('Found', len(config['dirs']), 'base directories')
        
        for base_dir_path in config['dirs']:
            self.base_directories.append(BaseDirectory(os.path.abspath(base_dir_path)))
        
        print('Loading existing metadata')
        for base_dir in self.base_directories:
            self.metadata.update(base_dir.get_metadata())
            
        print('Scanning for new files')
        for base_dir in self.base_directories:
            new_directory_metadata = base_dir.get_metadata()
            for file_path in base_dir.get_files_without_metadata():
                try:
                    with Image.open(file_path) as img:
                        digest = self.calculate_checksum(file_path)
                        file_metadata = {'type': 'image', 'digest': digest, 'base_directory_path': base_dir.get_path()}
                        # search for digest in other files, if found - copy metadata
                        for entry in self.metadata.values():
                            if entry['digest'] == digest:
                                file_metadata = copy.deepcopy(entry)
                                file_metadata['base_directory_path'] = base_dir.get_path()
                        new_directory_metadata[file_path] = file_metadata
                except:
                    new_directory_metadata[file_path] = {'type': 'generic'}
            base_dir.set_metadata(new_directory_metadata)
            self.metadata.update(base_dir.get_metadata())
            
        print('Removing entries for missing files')
        for base_dir in self.base_directories:
            new_directory_metadata = base_dir.get_metadata()
            for path in list(new_directory_metadata.keys()):
                if not os.path.exists(path) or not os.path.isfile(path):
                    print('Removing entry for file', path)
                    del new_directory_metadata[path]
                    del self.metadata[path]
            base_dir.set_metadata(new_directory_metadata)
        
        print(f'Loaded {len(self.metadata)} metadata entries')
    
    
    def calculate_checksum(self, file_path, algorithm='sha512'):
        hash_func = hashlib.new(algorithm)
        with open(file_path, "rb") as f:
            while chunk := f.read(4096):  # Read the file in chunks to avoid memory issues
                hash_func.update(chunk)
        return hash_func.hexdigest()


    def search_images(self, search_conditions):
        return self.files
