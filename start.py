from flask import Flask
from src.initialization import Gallery

gallery = Gallery()

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"