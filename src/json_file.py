import copy
import json
import os


class JsonFile:
    def __init__(self, path, default={}):
        self.path = path
        if not os.path.exists(self.path):
            self.set_data(default)
        else:
            with open(self.path, 'r') as file:
                self.data = json.load(file)

    def get_data(self):
        return copy.deepcopy(self.data)


    def set_data(self, data):
        with open(self.path, 'w') as file:
            json.dump(data, file, sort_keys=True, indent=4)
        self.data = copy.deepcopy(data)
