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
def list():
    path = request.args.get('path')

    dirs = [(b['path'], b['path']) for b in Config().branches().get_all()]
    for dir in dirs:
            
    if path != None:
        path_items = os.listdir(path)
        dirs = [(item, os.path.join(path, item)) for item in path_items if os.path.isdir(os.path.join(path, item))]
        files = [(item, os.path.join(path, item)) for item in path_items if os.path.isfile(os.path.join(path, item))]

    return render_template('list.html', dir_items=dirs, file_items=files, )


@app.route('/file/<path:filepath>')
def image(filepath):
    return send_from_directory(os.path.dirname(filepath), os.path.basename(filepath))


@app.route('/rescan')
def rescan():
    return {'status': 'ok'}