from src.gallery_branch import GalleryBranch
from src.json_file import JsonFile


# Main responsibilities of class:
#   1. Main API for searching gallery - searching is delegated to branches
#   2. Configuration API
class Gallery:
    def __init__(self, conf_file_path):
        self.conf_file = JsonFile(conf_file_path, {"dirs": []})
        self.branches = []
        for path in self.conf_file.load()['dirs']:
            self.branches.append(GalleryBranch(path))
        
        
    # load all albums - directories with content
    # load all metadata into collection
    # check every album for new files and add metadata, checking for same digest
    # check every album for missing files and delete unnecessary metadata
    
    
    def get_entries(self, search_condition):
        result = []
        for branch in self.branches:
            result.extend(branch.get_entries(search_condition))
        return result
    
    
    # id - absolute path of file
    def get_entry_by_id(self, id):
        pass