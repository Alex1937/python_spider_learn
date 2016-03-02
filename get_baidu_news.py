# -*- coding: utf-8 -*-
__author__ = 'alex'

import chardet
import urllib2
from bs4 import BeautifulSoup

'''
分析百度热点新闻
难点: 不像分析zhihu的问题,每个a标签都有固定的class, 这边需要分析新闻的上层标签

'''

baidu_news = "http://news.baidu.com/"


class PicSpider:

    def __init__(self, data):
        self.url = data.get('url')


    def browser(self):
        "开始浏览百度新闻页面"
        req = urllib2.Request(self.url)
        response = urllib2.urlopen(req, timeout=10).read()

        "处理中文编码"
        coding_response = chardet.detect(response)
        if coding_response['encoding'] == 'utf8' or coding_response['encoding'] == 'UTF-8':
            html = response
        else:
            html = response.decode('gb2312', 'ignore').encode('utf8')

        "构造soup对象"
        soup = BeautifulSoup(html, 'html.parser')
        reg_soup = soup.find_all('ul', class_='ulist focuslistnews')
        for child in reg_soup:
            anchor = child.find_all('a')
            for sub_child in anchor:
                print sub_child.string, " 访问地址:", sub_child.get('href')

data = {'url': baidu_news}
baidu = PicSpider(data)
baidu.browser()
