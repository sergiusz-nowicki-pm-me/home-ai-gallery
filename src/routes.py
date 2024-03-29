import sqlite3
from flask import render_template
from src.gallery import Gallery


class Routes:
    def __init__(self):
        db = sqlite3.connect('./config/test.db')
        self.gallery = Gallery(db)


    def branch_add(self, path):
        self.gallery.get_branches.add(path)
        return {'status': 'ok'}
    

    def config(self):
        return render_template('config.html')