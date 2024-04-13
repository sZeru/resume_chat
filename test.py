# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 11:52:38 2024

@author: cdare
"""

from flask import Flask
app = Flask(__name__)
@app.route('/')
def hello():
    return 'Hello World!'