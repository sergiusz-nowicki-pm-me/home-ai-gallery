from flask import render_template
from src.branches import Branches


class Config():
    def __init__(self):
        self.branches_list = []


    def branches(self):
        return Branches()


    def view(self):
        return render_template("config.html")