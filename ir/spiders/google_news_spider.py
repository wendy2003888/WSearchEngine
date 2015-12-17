#-*- coding:utf-8 -*-

from urllib2 import Request, urlopen, URLError
import re
from bs4 import BeautifulSoup
from multiprocessing import Pool
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11"
headers = { 'User-Agent' : user_agent }
out = open('news.txt','w')


class Spider:
    def __init__(self):
        self.items = []
        self.respos = None

    def load(self):
        try:
            starturls = ['https://news.google.com/','https://news.google.com/news/section?cf=all&pz=1&topic=tc']
            for starturl in starturls:            
                request = Request(starturl, headers = headers)
                self.respons = urlopen(request)
                respons = urlopen(request)
                content = respons.read()
                # pattern = re.compile()
    #            t = re.findall(r'h2 class="esc-lead-article-title".*?>(.*?)</h2>', content)
    #            for p in t:
    #                title, url = re.search(r'href="(.*?)"',p).group(1), re.search(r'<span.*?>(.*?)</span>',p).group(1)
                self.soup = BeautifulSoup(content,"html5lib")
                piece = self.soup.find_all("h2",attrs={"class":"esc-lead-article-title"})
                for p in piece:
                    url, title, description  = p.a['href'], p.a.span.string, p.parent.parent.find_all('div', attrs={'class':'esc-lead-snippet-wrapper'})[0].string
    #                print description, title, url 
                    self.getContent(title, url, description)
        except URLError, e:
            print e.reason

    def getContent(self, title, url, description):
        try:
            if url:
                request = Request(url, headers = headers)
                content = urlopen(request).read()
                details = re.findall(r'<p.*?>(.*?)</p>',content)
                detail = ''
                for d in details:
                    detail += d
                #print description, type(title), type(url), detail
                if title==None:
                    title='title'
                if detail == None:
                    detail='detail'
                if url==None:
                    url='url'
                out.write(str(title).decode('utf-8') +'####'+url.decode('utf-8')+'####'+detail.decode('utf-8')+'####'+description.decode('utf-8')+'#####')
            return [title, url, detail]
        except Exception,e:
            print 'Fail',e
            return False


    def run(self):
        try:
            self.load()
            return True
        except Exception,e:
            print 'Fail:',e
            return False

# output = open('out.txt', 'w+')
sp = Spider()
sp.run()
