import sqlite3
from src.gallery import Gallery


class Routes:
    def __init__(self):
        db = sqlite3.connect('./config/test.db')
        self.gallery = Gallery(db)


    def branch_add(self, path):
        self.gallery.get_branches.add(path)
        return {'status': 'ok'}