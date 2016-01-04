#/usr/bin/env python
#-*-coding:utf-8-*-
import config,re,os
from multiprocessing import Pool,Lock
from myutil import httptools
import logging
import logging.config

regex_listing = re.compile(r'<span class="listingscnt"\s*>(.*?)</span>')
regex_num = re.compile('[\d,]+')

logging.config.fileConfig("./log/logging.conf")    # 采用配置文件  
logger1 = logging.getLogger("logger1")   
logger2 = logging.getLogger("logger2") 
    
def get_root_listings():
    root_cate = config.root_category_id
    url = config.url.replace('[category]',root_cate)
    tool=httptools.httptools()
    html = tool.gethtml(url)
    num = regex_listing.search(html)
    if num != None:
        num = num.group(1)
        num = regex_num.search(num)
        if num != None:
            num = num.group()
            num = num.replace(',','')
            if num != '':
                return num
    return 0  
    
if __name__=='__main__':
    try:
        listings_count = get_root_listings()
        print config.root_name,listings_count
    except Exception,e:
        logger2.error(str(e))

