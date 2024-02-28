import os
from flask import Flask, send_from_directory
from src.gallery import Gallery


gallery = Gallery('./config/conf.json')
app = Flask(__name__)


@app.route("/")
def hello_world():
    return '<br/>'.join([f.get_name() + f.get_preview() for f in gallery.search_images("*")])


@app.route('/image-preview/<path:filepath>')
def image_preview(filepath):
    return send_from_directory(os.path.dirname(filepath), os.path.basename(filepath))


@app.route('/image/<path:filepath>')
def image(filepath):
    return send_from_directory(os.path.dirname(filepath), os.path.basename(filepath))