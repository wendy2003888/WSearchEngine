
from __init__ import *
from model import Spider, IMDBitem, newsItem



class storeItem(object):

    def store(self, item, spider):
        obj = {'chname': '', 'orgname' : '', 'year' : '',
        'country' : '', 'imdbScor': '', 'imdbUrl' :'', 'doubanScor' : '',
        'doubanUrl' : '', 'size': '', 'url' : ''}
        for k, v in item.iteritems():
            obj[k] = v
        data = Spider(obj['chname'], obj['orgname'], obj['year'],
        obj['country'], obj['imdbScor'], obj['imdbUrl'],
        obj['doubanScor'], obj['doubanUrl'], obj['size'], obj['url'])
        
        sp = session.query(Spider).filter(Spider.url == obj['url']).first()
        if sp is None:
            session.add(data)
            session.commit()
        session.close()

class storeIMDB(object):

    def store(self, item, spider):
        obj = {'orgname' : '', 'year' : '', 'country' : '', 
        'imdbScor': '', 'description' : '', 'storyline': '', 'url' : ''}
        for k, v in item.iteritems():
            obj[k] = v
        data = IMDBitem(obj['orgname'], obj['year'], obj['country'], 
            obj['imdbScor'], obj['description'], obj['storyline'], obj['url'])
        
        sp = session.query(IMDBitem).filter(IMDBitem.url == obj['url']).first()
        if sp is None:
            session.add(data)
            session.commit()
        session.close()

class storeIFENG(object):

    def store(self, item, spider):
        obj = {'title' : '', 'date' : '', 'content' : '', 'url' : '','orgUrl' : ''}
        for k, v in item.iteritems():
            if k == 'content':
                if v:
                    for i, s in enumerate(v):
                        if i > 0 :
                            c = c + ' ' + s 
                        else:
                            c = s
                    obj[k] = c
            else:
                obj[k] = v
        obj['content'] = re.sub(r'<.*?>','',obj['content'])
        data = newsItem(obj['title'], obj['date'], obj['content'], obj['url'])
        if 'orgUrl':
            data2 = newsItem(obj['title'], obj['date'], obj['content'], obj['orgUrl'])
            sp = session.query(newsItem).filter(newsItem.url == obj['orgUrl']).first()
            if sp is None:
                session.add(data2)
                session.commit()
        else:
            sp = session.query(newsItem).filter(newsItem.url == obj['url']).first()
            print sp,'#####'
            if sp is None:
                session.add(data)
                session.commit()
        session.close()