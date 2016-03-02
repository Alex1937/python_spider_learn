# -*- coding: utf-8 -*-
import re
import urllib
import urllib2
import cookielib

from bs4 import BeautifulSoup


loginurl = 'https://www.zhihu.com/login/email'
logindomain = 'https://www.zhihu.com'

# testurl = sys.argv[1]

testurl = "https://www.zhihu.com"

'''
定义一个类,把所有的信息封装起来, 重用性高
'''
class Login(object):

    def __init__(self):
        '''初始化用户信息'''
        self.xsrf = ''
        self.email = ''
        self.password = ''
        self.domain = ''

        '''
        声明一个CookieJar对象实例来保存cookie
        '''
        self.cj = cookielib.CookieJar()

        '''
        利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
        通过handler来构建opener
        '''
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        '''
        这里要注意的一个细节，使用 urllib2.install_opener() 会设置 urllib2 的全局 opener 这样后面的使用会很方便
        '''
        urllib2.install_opener(self.opener)


    def setLoginInfo(self, xsrf, email,  password, domain):
        '''设置用户登陆信息'''
        self.xsrf = xsrf
        self.email = email
        self.password = password
        self.domain = domain

    def login(self):
        '''登陆网站所需信息从chrome调试中得知'''
        loginparams = {'_xsrf': self.xsrf,
                       'email': self.email,
                       'password': self.password,
                       'remember_me': 'true'}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'}

        '''
        创建一个request
        和直接urlopen的区别是request可以传入的更加丰富
        '''
        req = urllib2.Request(self.domain, urllib.urlencode(loginparams), headers=headers)

        '''
        设置超时 10s
        '''
        response = urllib2.urlopen(req, timeout=10)
        '''
        response为一个对象, 需要通过read获得数据
        '''
        thePage = response.read()
        return thePage

    def browser(self, url):
        result = urllib2.urlopen(url)
        return result.read()

    def analysis(self, result):
        "将html文档转换成soup对象, 最简单的方式处理html文件"
        soup = BeautifulSoup(result, "html.parser")
        "根据标签属性匹配出zhihu上问题的<a>标签,获得的是soup对象数组"
        reg_list = soup.find_all('a', class_='question_link', href=re.compile(r'/question/\d+'))
        for child in reg_list:
            "打印匹配到的问题的<a>标签的内容"
            print child.string, "          访问地址:","https://www.zhihu.com" + child.get('href')


if __name__ == '__main__':
    userlogin = Login()
    "这类信息从chrome中源代码可以获得"
    xsrf = '879219dde1846ffe2743f5103d73d929'
    email = 'youremailaddress@163.com'
    password = 'ilovezhihu'
    domain = loginurl
    userlogin.setLoginInfo(xsrf, email, password, domain)
    thePage = userlogin.login()

    '''
    decode('unicode-escape')十分关键
    把字符串的unicode编码转换成真正的Unicode字节码
    '''
    # print thePage.decode('unicode-escape')

    result = userlogin.browser(testurl)
    userlogin.analysis(result)
