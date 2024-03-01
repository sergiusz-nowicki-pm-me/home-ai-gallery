import os
import sqlite3
from src.gallery_branch import GalleryBranch
from src.json_file import JsonFile


class Branches:
    def __init__(self, db):
        self.db = db


    def get_all(self):
        return [row[0] for row in self.db.execute('select path from branch').fetchall()]
    

    def add(self, path):
        if not os.path.isdir(path):
            raise Exception(f'Branch path "{path}" not exists')
        
        if path in self.get_all():
            raise Exception(f'Branch "{path}" is allready in gallery')
        
        print(f'Adding branch {path}')
        self.db.execute('insert into branch (path) values (:path)', {'path': path})
        self.db.commit()


# Main responsibilities of class:
#   1. Main API for searching gallery - searching is delegated to branches
#   2. Configuration API
class Gallery:
    def __init__(self, db):
        self.db = db

        with open('src/sql/init.sql') as f:
            self.db.executescript(f.read())


    def get_branches(self):
        return Branches(self.db)


    def rescan(self):
        pass
    
    # load all albums - directories with content
    # load all metadata into collection
    # check every album for new files and add metadata, checking for same digest
    # check every album for missing files and delete unnecessary metadata
    
    
    # def get_entries(self, search_condition):
    #     result = []
    #     for branch in self.branches:
    #         result.extend(branch.get_entries(search_condition))
    #     return result
    
    
    # # id - absolute path of file
    # def get_entry_by_id(self, id):
    #     pass