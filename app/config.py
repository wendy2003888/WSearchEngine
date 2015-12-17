#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os

SECRET_KEY = 'be a Phantom'

BASE_DIR = os.getcwd()
SQLALCHEMY_DATABASE_URI =  'mysql://' + 'wendy2003888' + ':' + 'wendy2003888' \
                 + '@' + 'localhost' + ':' + '3306'  + os.sep + 'irapp' + '?charset=utf8&use_unicode=0'

SQLALCHEMY_POOL_RECYCLE = 10
PER_PAGE = 20


