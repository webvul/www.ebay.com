#/usr/bin/env python
#-*-coding:utf-8-*-
from myutil import httptools
import config
import re,os
from multiprocessing import Pool,Lock
import logging
import logging.config

logging.config.fileConfig("./log/logging.conf")    # 采用配置文件  
logger1 = logging.getLogger("logger1")   
logger2 = logging.getLogger("logger2") 

regex_listing = re.compile(r'<span class="listingscnt"\s*>(.*?)</span>')
regex_num = re.compile('[\d,]+')

low_price=re.compile('_udlo=&')
high_price=re.compile('_udhi=&')

regex_name = re.compile(r'/sch/(.*?)/.*?&_udlo=(.*?)&_udhi=(.*?)&_dmd=1')

def get_listings(url):#没有解析出listings的html文件记录下来。
    try:
        for i in range(3):
            html = tool.gethtml(url)
            if html.find('We were unable to run the search you entered. Please try again in a few minutes.') == -1:
                break
        num = regex_listing.search(html)
        if num != None:
            num = num.group(1)
            num = regex_num.search(num)
            if num != None:
                num = num.group()
                num = num.replace(',','')
                if num != '':
                    return num
        if num == None or num == '':
            name = regex_name.search(url)
            if name != None:
                cate = name.group(1)
                udlo = name.group(2)
                udhi = name.group(3)
            name = config.category_listings_path+cate+'_'+udlo+'_'+udhi+'.html'
            
            lock.acquire()
            f = open(name,'w')
            f.write(html)
            f.flush()
            f.close()
            lock.release()
            return 
    except Exception,e:
        logger2.error(url+'\t'+'num:'+str(num)+'\n'+str(e))

def dichotomy(low,high,url):        
    try:
        if high!='':
            mid=int((int(low)+int(high))/2)
        else:
            mid=low+100
        url_split=url.replace('_udlo=','_udlo='+str(low)).replace('_udhi=','_udhi='+str(mid))
        num = get_listings(url_split)
        if num == None:
            return
        listings_count=int(get_listings(url_split))
        if listings_count<=9800:
            lock.acquire()
            f_suit_url.write(str(listings_count)+'\t'+url_split+'\n')
            f_suit_url.flush()
            lock.release()
        else:
            if int(mid)-int(low)==1:   
                lock.acquire()
                f_suit_url.write(str(listings_count)+'\t'+url_split+'\n')
                f_suit_url.flush()
                lock.release()
            else:
                dichotomy(low,mid,url)
        url_split=url.replace('_udlo=','_udlo='+str(mid)).replace('_udhi=','_udhi='+str(high))
        listings_count=int(get_listings(url_split))  
        if high!='':
            if listings_count<9800:
                if listings_count!=0:
                    lock.acquire()
                    f_suit_url.write(str(listings_count)+'\t'+url_split+'\n')
                    f_suit_url.flush()
                    lock.release()
            else:
                if int(high)-int(mid)==1:   
                    lock.acquire()
                    f_suit_url.write(str(listings_count)+'\t'+url_split+'\n')
                    f_suit_url.flush()
                    lock.release()
                else:
                    dichotomy(mid,high,url)
        else:
            if listings_count<9800:
                if listings_count!=0:
                    lock.acquire()
                    f_suit_url.write(str(listings_count)+'\t'+url_split+'\n')
                    f_suit_url.flush()
                    lock.release()
            else:
                dichotomy(mid,high,url)
    except Exception,e:
        logger2.error(url_split+'\t'+str(e))

def handle_url(line):
    try:
        line=line.split('\t')
        url=line[1].strip()
        low=0
        high=''
        dichotomy(low,high,url)
    except Exception,e:
        logger2.error(url+'\t'+str(e))

def get_suit_url():  
    global f_suit_url,lock,tool
    tool=httptools.httptools()
    lock=Lock()
    
    f=open(config.category_listings_path+'more_9800.csv')
    lines=f.readlines()
    f.close()
    
    f_suit_url=open(config.category_listings_path+'split_more9800.csv','w')  
     
    pool=Pool(15)
    pool.map(handle_url,lines)  
    pool.close()
    pool.join()  
     
    f_suit_url.close()

if __name__=='__main__':
    try:
        logger1.info('start split_more9800.py...')
        get_suit_url()
        logger1.info('over split_more9800.py')
        os.system('nohup python get_ids.py &')
    except Exception,e:
        print e
        logger2.error(str(e))
"""
1)读取more_9800.csv文件的url
2）获取html文件，解析listings，采用二分法拆分url使得
"""
        
