#-*- coding:utf-8 -*-

from app import app, views

if __name__ == '__main__':
    app.run(port = 8000, debug =True)