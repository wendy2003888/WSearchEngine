#-*- coding: utf-8 -*-
import re
from functools import wraps
from math import ceil
import nltk
from nltk.corpus import wordnet as wn
import jieba
import jieba.analyse

from flask import render_template, request, redirect, url_for

from app import app, SE
from sphinx import en_stopwd, cn_stopwd
from config import PER_PAGE

import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

def throw_exception(f):
    @wraps(f)
    def call(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception, e:
            print e
            return unicode(e)
    return call

def query_handler(q):
    '''
    处理查询
    英文和中文分别处理
    '''

    '''分别提取英文和中文单词集'''
    en = re.findall(r'\w+', q)
    cnPattern = re.compile(u'[\u4e00-\u9fa5]+')
    cn = re.findall(cnPattern, q)
    '''分词处理'''
    en_tokens = list(set([ w for s in en for w in nltk.word_tokenize(s) ]))
    cn_tokens = list(set([ w for s in cn for w in jieba.lcut_for_search(s)]))
    '''去除停用词'''
    en_cleans = [w for w in en_tokens if w.lower() not in en_stopwd]
    cn_cleans = [w for w  in cn_tokens if w.encode('utf-8') not in cn_stopwd]
    if not en_cleans:
        en_cleans = en_tokens
    if not cn_cleans:
        cn_cleans = cn_tokens
        
    # cn_cleans.append(jieba.analyse.extract_tags(s, topK=1))
    '''英文词干化'''
    porter =nltk.PorterStemmer()
    en_result= [porter.stem(t) for t in en_cleans]
    tokens = en_result + cn_cleans
    return  tokens



class Pagination(object):

    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    @property
    def total(self):
        return self.total_count
    

    def iter_pages(self, left_edge=1, left_current=2,
                   right_current=3, right_edge=1):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num

@app.route('/')
@throw_exception
def index():
    try:
        return render_template('index.html')
    except Exception, e:
        return unicode(e)

query = ''
q = []

@app.route('/search', methods = ['GET','POST'])
@app.route('/search/<int:page>/', methods = ['GET','POST'])
#@throw_exception
def search(page = 0):
    try:
        global query,q
        if request.method == 'POST':
            query = request.form['query']
            q = query_handler(query)
            st = 0
            page = 1
            res = SE.getResult(q,'*', st)
            results, time_dif = res[0], res[1]
            pagination = Pagination(page=page, total_count=res[2], per_page=PER_PAGE)
            query = query.encode('utf-8') if type(query) == type(u'') else query
            return render_template('results.html', results = results, q = query, time_dif=time_dif, pagination=pagination)
        else:
            if page != 0 and query != '':
                st = page * PER_PAGE
                res = SE.getResult(q,'*', st)
                results, time_dif = res[0], res[1]
                pagination = Pagination(page=page, total_count=res[2], per_page=PER_PAGE)
                return render_template('results.html', results = results, q = query.encode('utf-8'), time_dif=time_dif, pagination=pagination)
            else:

                return redirect(url_for('index'))
    except Exception, e:
        return unicode(e)

@app.route('/about')
@throw_exception
def about():
    try:
        return render_template('about.html')
    except Exception, e:
        return unicode(e)

