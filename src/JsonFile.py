import json
import os


class JsonFile:
    def __init__(self, path, default={}):
        self.path = path
        self.default = default
        
    def load(self):
        if not os.path.exists(self.path):
            self.save(self.default)
            
        with open(self.path, 'r') as file:
            data = json.load(file)
        return data

    def save(self, data):
        with open(self.path, 'w') as file:
            json.dump(data, file, sort_keys=True, indent=4)
