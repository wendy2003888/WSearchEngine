#-*- coding: utf-8 -*-

from flask import Flask
from sphinx import QuerySphinx

Flask_ETTINGS = '../config.py'

app = Flask(__name__)
app.config.from_pyfile(Flask_ETTINGS, silent = False)

SE = QuerySphinx.Search()


