import os
import sqlite3
from flask import Flask, render_template, send_from_directory
from src.gallery import Gallery
from src.routes import Routes


app = Flask(__name__)


@app.route('/')
def index():
    with sqlite3.connect('./config/test.db') as db:
        gallery = Gallery(db)
        entries = []
        print(entries)
        return render_template('column-gallery.html', entries=entries)


@app.route('/branch/add/<path>')
def branch_add(path):
    return Routes().branch_add(path)


@app.route('/image/<path:filepath>')
def image(filepath):
    return send_from_directory(os.path.dirname(filepath), os.path.basename(filepath))


@app.route('/rescan')
def rescan():
    return {'status': 'ok'}