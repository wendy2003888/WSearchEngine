# -*- coding: utf-8 -*-

from __init__ import BaseModel
from sqlalchemy import Column
from sqlalchemy.types import CHAR, Integer, String


class Spider(BaseModel):
    __tablename__= 'piaohua'
    _id = Column(Integer, primary_key=True)
    chname = Column(String(300))
    orgname = Column(String(300))
    year = Column(String(50))
    country = Column(String(50))
    imdbScor = Column(String(100))
    imdbUrl = Column(String(100))
    doubanScor = Column(String(50))
    doubanUrl = Column(String(100))
    size = Column(String(50))
    url = Column(String(500))

    def __init__(self, chname, orgname, year, country, imdbScor, imdbUrl,
        doubanScor, doubanUrl, size, url):
        self.chname = chname
        self.orgname = orgname
        self.year = year
        self.country = country
        self.imdbScor = imdbScor
        self.imdbUrl = imdbUrl
        self.doubanScor = doubanScor
        self.doubanUrl = doubanUrl
        self.size = size
        self.url = url



class IMDBitem(BaseModel):
    __tablename__= 'imdb'
    _id = Column(Integer, primary_key=True)
    orgname = Column(String(300))
    year = Column(String(50))
    country = Column(String(50))
    imdbScor = Column(String(100))
    description = Column(String(100000))
    storyline = Column(String(100000))
    url = Column(String(500))

    def __init__(self, orgname, year, country, imdbScor, description,
        storyline, url):
        self.orgname = orgname
        self.year = year
        self.country = country
        self.imdbScor = imdbScor
        self.description = description
        self.storyline = storyline
        self.url = url

    def __repr__(self):  
        return "<item('%s','%s')>" % (self._id, self.url)


class newsItem(BaseModel):
    __tablename__= 'news'
    _id = Column(Integer, primary_key=True)
    title = Column(String(300))
    date = Column(String(50))
    content = Column(String(100000))
    url = Column(String(500))

    def __init__(self, title, date, content, url):
        self.title = title
        self.date = date
        self.content = content
        self.url = url

    def __repr__(self):  
        return "<item('%s','%s')>" % (self._id, self.url)
