# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 11:52:38 2024

@author: cdare
"""
from flask import Flask
from flask import render_template

app = Flask(__name__)
@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/ask')
def ask():
    return render_template('ask.html')

app.run(host="0.0.0.0", port=80)