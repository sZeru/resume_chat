# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 16:30:48 2024

@author: cdare
"""

import os
import requests

pdfFile="SOFI-2023.pdf"
if not os.path.exists(pdfFile):
    throw Exception('Well looks like the file we need cant be found')
else:
    print("SOFI exists.")