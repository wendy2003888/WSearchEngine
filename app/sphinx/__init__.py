#-*- coding:utf-8 -*-


from nltk.corpus import stopwords
import jieba
jieba.load_userdict('./sougou.txt')

en_stopwd = stopwords.words('english')
cn_stopwd = [line.rstrip() for line in open('./sphinx/stopwords_cn_zh.txt', 'r')]