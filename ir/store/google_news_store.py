# -*- coding: utf-8 -*-
from __init__ import *
from model import newsItem

i = 0
content = open('../googleNewsData/news_12163.txt','r').read()
lines = content.split('#####')    #title, url, detail, description
for line in lines:
    info = line.split('####')
    print i
    i += 1
    if len(info) < 2:
        continue 
    title = info[0] if info[0] != 'title' else ''
    url = info[1] if info[1] != 'url' else ''
    if len(info) >= 3:
        if info[2] == '':
            if len(info) == 4 and info[3] != '':
                detail = info[3]
            else:
                detail = ''
        else:
            detail = info[2]
    else:
        detail = ''

    # print title + '###'+ url+'^^^^^'+detail

    data = newsItem(title, '2015-12-16',detail, url)
    sp = session.query(newsItem).filter(newsItem.url == url).first()
    if sp is None:
        session.add(data)
session.commit()
session.close()
