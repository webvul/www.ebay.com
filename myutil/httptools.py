#/use/bin/env python
#coding:utf-8
'''
httptools by snike
'''
import urllib2,cookielib
import os,zlib
import logging as httplog
import random
from gzip import GzipFile
from StringIO import StringIO
from logtool import logtool
from cgitb import html
httplog=logtool('httplog','http.log')
class httptools:

    def __init__(self):
        self.__head={}
        self.__cookie='npii=bcguid/c211261e14a0a629a5d60816fe0a6dc2568e1af4^tguid/c211183014a0a5e069cc37cffff4eba6568e1af4^; JSESSIONID=8F1402D84442F8D42C15FA4C7D91ACC5; ns1=BAQAAAUq3ZBmUAAaAANgATlaOHEVjNzR8NjAxXjE0MjA2MTI2MzMwNjFeXjBeMnw0fDF8NDJ8NDN8MTBeMV40XjReM14xMl4xMl4yXjFeMV4wXjBeMF4xXjY0NDI0NTkwNzVQIkfuB7fBb6HZfcgaA6RCw3IJ8w**; cssg=c2d726dd14a0a56704a10234fff43f85; s=CgAD4ACBUrjpFYzJkNzI2ZGQxNGEwYTU2NzA0YTEwMjM0ZmZmNDNmODUA7gDGVK46RTMGaHR0cDovL3d3dy5lYmF5LmNvbS9zY2gvaS5odG1sP19mcm9tPVI0MCU3Q1I0MCZfc2FjYXQ9MCZfdWRsbz0mX3VkaGk9Jl9mdHJ0PTkwMSZfZnRydj0xJl9zYWJkbG89Jl9zYWJkaGk9Jl9zYW1pbG93PSZfc2FtaWhpPSZfc2FkaXM9MTUmX3N0cG9zPSZfc29wPTEyJl9kbWQ9MSZfbmt3PVBhcnJvdCtEcm9uZStQYXJ0cyZMSF9Mb2NhdGVkSW49MYEBus8*; nonsession=CgADKACBeEupFYzIxMTE4MzAxNGEwYTVlMDY5Y2MzN2NmZmZmNGViYTYAywACVKzvzTc1vZ85fA**; lucky9=2089857; ds2=sotr/b7pQ5zQMz1zz^ssts/1420617932257^; dp1=bpbf/#40000000000810042000000586f4fc9^tzo/-1e0586f4fcc^abtc/054ade401^u1p/QEBfX0BAX19AQA**568e1c45^bl/CN586f4fc5^idm/154ae2584^; ebay=%5Ecv%3D15555%5Ejs%3D1%5Esbf%3D%2341400000c00100000160210%5Epsi%3DAYKKrric*%5E'
        self.__head['Accept']='text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
#		self.__head['Accept-Charset']=''
        self.__head['Accept-Language']='en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4'
        # self.__head['Cache-Control']='max-age=0'
#		self.__head['Authorization']=''
        self.__head['Connection']='keep-alive'
#		self.__head['Content-Length']=''
        self.__head['Cookie']=self.__cookie
        self.__head['Host']='www.ebay.com'
#		self.__head['Pragma']=''
        # self.__head['Referer']='http://www.ebay.com/'
        self.__head['User-Agent']='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        self.__proxylist=None
    def gethtml(self,url,data=None,heads='FHBJ<KGFYOLL'):
        if heads=='FHBJ<KGFYOLL':
            heads=self.__head
        if not heads:
            heads={}
        content=''
        count=0
        while True:
            try:
                req=urllib2.Request(url,data,{})
                content=urllib2.urlopen(req,timeout=10).read()
                print 'success:',url
                return content
            except Exception,e:
                httplog.info(e)
                if "404" in str(e):
                    print '404',url
                    return str(e)
                count+=1
                print e,url,'crawl once more:'+str(count)
                if count==6:
                    return str(e)
    def sgethtml(self,url):
        return self.gethtml(url,None,None)
    #抓取图片
    def get_img(self,url):
        heads = {"User-agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"}
        req = urllib2.Request(url,None,{})
        img_String = urllib2.urlopen(req).read()
        return img_String
        
    def gethtmlproxy(self,url,data=None,heads='FHBJ<KGFYOLL'):
        if not self.__proxylist:
            if os.path.exists('./myutil/proxylist.txt'):
                f=open('./myutil/proxylist.txt')
            else:
                f=open('proxylist.txt')
            self.__proxylist=f.readlines()
            f.close()
#         proxy_support = urllib2.ProxyHandler({'http':'http://'+random.choice(self.__proxylist)})
        if heads=='FHBJ<KGFYOLL':
            heads=self.__head
        if not heads:
            heads={}
        count=0
        while True:
            try:
                proxy_support = urllib2.ProxyHandler({'http':'http://'+random.choice(self.__proxylist)})
                opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)  
                req=urllib2.Request(url,data,{})
                res=urllib2.urlopen(req,timeout=30)
                content=res.read()
                return content
            except Exception,e:
                print e
                httplog.info(e)
                if "404" in str(e):
                    return str(e)     
                count+=1
                if count==3:
                    return str(e)
    def sgethtmlproxy(self,url):
        return self.gethtmlproxy(url,None,None)
if __name__=='__main__':
    tool=httptools()
#     html=tool.sgethtml('http://blog.ii8go.com/asdsadasdasdsa')
#     with open('test.html','w') as f:
#         f.write(html)
    html=tool.get_img('http://i.ebayimg.com/00/s/ODAwWDgwMA==/z/-kcAAOSw7aBVCWZu/$_14.JPG')
    print html
