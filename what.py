# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 16:41:56 2024
I think this is supposed to communicate with the templates
@author: cdare
"""

import pika
from flask import Flask
from flask import render_template, request
# Send form data to the asker