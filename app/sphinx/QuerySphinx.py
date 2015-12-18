#-*- coding:utf-8 -*-

import sys, time
sys.path.append("..")

from ir.store import session
from ir.store.model import IMDBitem, newsItem
from sphinxapiOld import *
import re


class Search():
    def __init__(self):
        self.cl = SphinxClient()
        self.mode = SPH_MATCH_ALL
        self.cl.SetMatchMode ( self.mode )
        self.cl.SetSortMode( SPH_SORT_EXTENDED, '@relevance DESC, @id DESC')


    def getResult(self, q, index, start):
        self.cl.SetLimits(offset = start, limit = 20)
        m = []
        for w in q:
            print w
            self.cl.AddQuery (w, index)
        t1 = time.clock()
        res = self.cl.RunQueries()
        t2 = time.clock()
        total = td = 0
        if res:
            for r in res:
                total += int(r['total_found'])
                td += float(r['time'])
                if r.has_key('matches'):
                    n = 1
                    #print '\nMatches:'
                    for match in r['matches']:
                        #print match
                        attrsdump = ''
                        for k , v in match['attrs'].items():
                            attrsdump = '%s, %s=%s' % ( attrsdump, k, v )
                        #print '%d. doc_id=%s, weight=%d%s' % (n, match['id'], match['weight'], attrsdump)
                        n += 1
                        source = match['attrs']['tid']
                        opts = {'before_match':'<span>', 'after_match':'</span>', 'chunk_separator': '...', 'around': 3}
                        title_opts = {'before_match':'<span>', 'after_match':'</span>', 'chunk_separator': '', 'around': 8}
                        if source == 1:
                            data = session.query(IMDBitem).filter_by(_id = match['id']).first()
                            if data:
                                w = r['words'][0]['word']
                                title = self.cl.BuildExcerpts([data.orgname], 'imdb',w, title_opts)
                                t = detail = ''
                                if not title:
                                    print 'ERROR:', cl.GetLastError()
                                    for i in title:
                                        t += i
                                detail = ''
                                res = self.cl.BuildExcerpts([data.country, data.imdbScor, data.description, data.storyline], 'imdb',w, opts)
                                if not res:
                                    print 'ERROR:', cl.GetLastError()
                                else:
                                    for entry in res:
                                        detail += entry
                                m.append(( data.url, title[0], detail))
                        elif source == 2:
                            data = session.query(newsItem).filter_by(_id = match['id']).first()
                            # print data, data.title, data.date, data.content
                            if data:
                                w = r['words'][0]['word']
                                title = self.cl.BuildExcerpts([data.title], 'news',w, title_opts)
                                t = detail = ''
                                if not title:
                                    print 'ERROR:', cl.GetLastError()
                                else:
                                    for i in title:
                                        t += i

                                res = self.cl.BuildExcerpts([data.date, data.content], 'news',w, opts)
                                if not res:
                                    print 'ERROR:', cl.GetLastError()
                                else:
                                    for entry in res:
                                        detail += entry
                                print t
                                m.append(( data.url, t.decode('utf-8'), detail.decode('utf-8')))
        return (m, td, total)
        
    

# if __name__ == "__main__":
#     main = Search()
#     main.getResult('Forest', 'imdb')
#eof