import os
import sqlite3
from flask import Flask, render_template, request, send_from_directory
from src.gallery import Gallery
from src.routes import Routes
from src.config import Config


app = Flask(__name__)

@app.route('/config')
def config():
    return Config().view()


@app.route('/config/branches')
def config_branches():
    return Config().branches().get_all()


@app.route('/config/branches/add')
def config_branches_add():
    path = request.args.get('path')
    branches = Config().branches()
    return branches.add(path)


@app.route('/config/branches/remove')
def config_branches_remove():
    md5 = request.args.get('md5')
    branches = Config().branches()
    return branches.remove(md5)


@app.route('/list')
def index():
    path = request.args.get('path')

    dirs = []
    files = []
    if path != '.':
        path_items = os.listdir(path)
        dirs = [path for path in path_items if os.path.isdir(os.path.join(path, path_items))]
        files = [path for path in path_items if os.path.isfile(os.path.join(path, path_items))]
    else:
        dirs = [b['path'] for b in Config().branches().get_all()]

    
    return render_template()
    # with sqlite3.connect('./config/test.db') as db:
    #     gallery = Gallery(db)
    #     entries = []
    #     print(entries)
    #     return render_template('column-gallery.html', entries=entries)


@app.route('/image/<path:filepath>')
def image(filepath):
    return send_from_directory(os.path.dirname(filepath), os.path.basename(filepath))


@app.route('/rescan')
def rescan():
    return {'status': 'ok'}