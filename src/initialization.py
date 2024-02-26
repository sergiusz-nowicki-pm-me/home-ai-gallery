import copy
import hashlib
import json
import os
from PIL import Image

METADATA_FILE_NAME = '.home-ai-gallery-metadata'

class JsonFile:
    def __init__(self, path, default={}):
        self.path = path
        self.default = default
        
    def load(self):
        if not os.path.exists(self.path):
            self.save_json_file(self.path, self.default)
            
        with open(self.path, 'r') as file:
            data = json.load(file)
        return data

    def save(self, data):
        with open(self.path, 'w') as file:
            json.dump(data, file, sort_keys=True, indent=4)


class Configuration(JsonFile):
    def __init__(self, path):
        super(path, {"dirs": []})
        
        
class BaseDirectory:
    METADATA_FILE_NAME = '.home-ai-gallery-metadata'
    
    def __init__(self, path):
        self.path = path
        self.metadata_file_path = os.path.join(self.path, self.METADATA_FILE_NAME)
        self.json_file = JsonFile(path)
        
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
        self.initialize()

    def initialize(self):        
        print('Loading configuration file')
        file_path = 'config/conf.json'
        config = self.load_json_file(file_path, default={"dirs": []})
        print('Found', len(config['dirs']), 'base directories')
        
        for base_dir_path in config['dirs']:
            self.base_directories.append(BaseDirectory(base_dir_path))
        
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
            self.metadata.update(self.base_dir.get_metadata())
            
        print('Removing entries for missing files')
        for base_dir_path in config['dirs']:
            new_directory_metadata = self.load_base_directory_existing_metadata(base_dir_path)
            for path in list(new_directory_metadata.keys()):
                if not os.path.exists(path) or not os.path.isfile(path):
                    print('Removing entry for file', path)
                    del new_directory_metadata[path]
                    del self.metadata[path]
            self.save_base_directory_metadata(base_dir_path, new_directory_metadata)
        
        print(f'Loaded {len(self.metadata)} metadata entries')
        
        
        
    def load_base_directory_existing_metadata(self, path):
        print('Loading metadata from ', path)
        metadata_file_path = os.path.join(path, METADATA_FILE_NAME)
        return self.load_json_file(metadata_file_path)


        
    def load_base_directory_metadata_with_new_files(self, path):
        existing_metadata = self.load_base_directory_existing_metadata(path)
        print('Scanning for new files in directory', path)
        for file_path in self.get_all_files(path):
            if file_path not in existing_metadata:
                print('New file found', file_path)
                try:
                    with Image.open(file_path) as img:
                        digest = self.calculate_checksum(file_path)
                        file_metadata = {'type': 'image', 'digest': digest, 'base_directory_path': path}
                        # search for digest in other files, if found - copy metadata
                        for entry in self.metadata.values():
                            if entry['digest'] == digest:
                                file_metadata = copy.deepcopy(entry)
                                file_metadata['base_directory_path'] = path
                        existing_metadata[file_path] = file_metadata
                except:
                    existing_metadata[file_path] = {'type': 'generic'}
        return existing_metadata   


        
    def get_all_files(self, path):    
        all_files = []
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                if file != METADATA_FILE_NAME:
                    all_files.append(file_path)
        return all_files



    def calculate_checksum(self, file_path, algorithm='sha512'):
        hash_func = hashlib.new(algorithm)
        with open(file_path, "rb") as f:
            while chunk := f.read(4096):  # Read the file in chunks to avoid memory issues
                hash_func.update(chunk)
        return hash_func.hexdigest()



    def save_base_directory_metadata(self, path, data):
        self.save_json_file(os.path.join(path, METADATA_FILE_NAME), data)
        


    def load_json_file(self, file_path, default={}):
        if not os.path.exists(file_path):
            self.save_json_file(file_path, default)
            
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data



    def save_json_file(self, file_path, data):
        with open(file_path, 'w') as file:
            json.dump(data, file, sort_keys=True, indent=4)
