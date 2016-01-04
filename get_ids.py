#/usr/bin/env python
#-*-coding:utf-8-*-
from myutil import httptools
import config
from common import *
from myutil.logtool import logtool
import re,os,time
from multiprocessing import Pool,Lock
import logging
import logging.config
import math

logging.config.fileConfig("./log/logging.conf")    # 采用配置文件  
logger1 = logging.getLogger("logger1")   
logger2 = logging.getLogger("logger2") 


regex_listing = re.compile(r'<span class="listingscnt"\s*>(.*?)</span>')
regex_num = re.compile('[\d,]+')

conn_items_regx=re.compile('<html[\s\S]*?items found from eBay international sellers')
asin_regx=re.compile('listingId="(.*?)"')

regex_name = re.compile(r'/sch/(.*?)/.*?&_udlo=(.*?)&_udhi=(.*?)&_dmd=1')

def get_listings(url,html):#没有解析出listings的html文件记录下来。
    try:
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

def get_asin_list(html):
    conn_itmes=conn_items_regx.search(html)
    if conn_itmes!=None:
        html=conn_itmes.group()
    asins_list=asin_regx.findall(html)
    return asins_list

def handle(line):
    try:
        line=line.split('\t')
        listings = int(line[0])
        if listings == 0:
            return
        url_homePage=line[1].strip()
        ids_result=[]
        for page in range(1,50):
            url=url_homePage.replace('_pgn=1','_pgn='+str(page))
            for j in range(3):
                html=tool.gethtml(url)
                if html.find('We were unable to run the search you entered. Please try again in a few minutes.') == -1:
                    break
                elif j == 2:
                    logger2.warning('We were unable to run the search you entered. Please try again in a few minutes.'+'\n'+url)
            if page == 1:
                listings_count = get_listings(url_homePage,html)
                listings_count_float = float(listings_count)
                page_count = math.ceil(listings_count_float/200)
                page_count = int(page_count)
            conn_itmes=conn_items_regx.search(html)
            if conn_itmes!=None:
                html=conn_itmes.group()
            asins_list=asin_regx.findall(html)
            ids_result.extend(asins_list)
            if page == page_count:
                break
#         ids_result = list(set(ids_result))
        if len(ids_result)!=0:        
            lock.acquire()
            f_asins.write('\n'.join(ids_result))
            f_asins.write('\n')
            f_asins.flush()
            f_success.write(str(listings_count)+'\t'+str(len(ids_result))+'\t'+url_homePage+'\n')
            f_success.flush()
            lock.release()
        else:
            logger2.warning('ids_result==[]'+'\n'+url_homePage)
    except Exception,e:
        logger2.error(url_homePage+'\t'+str(e))
    
def get_info():
    global lock,f_success,f_asins,tool
    lock=Lock()
    tool=httptools.httptools()
    
    f1=open(config.category_listings_path+'less_9800.csv')
    lines=f1.readlines()
    f1.close()
    f2=open(config.category_listings_path+'split_more9800.csv')
    lines2=f2.readlines()
    f2.close()
    lines.extend(lines2)
    
    f_asins=open(config.get_ids_path+'ids.csv','w')
    f_success = open(config.get_ids_path+'success_url.csv','w')
    f_success.write('listings_count'+'\t'+'id_count'+'\t'+'url'+'\n')
    f_success.flush()
    
    pool=Pool(15)
    pool.map(handle,lines)
    pool.close()
    pool.join()
    
    f_asins.close()
    f_success.close()

if __name__=='__main__':
    try:
        logger1.info('start get_ids.py...')
        get_info()#得到每个品类下的listings asins url 和asin列表
        sentence='sort '+config.get_ids_path+'ids.csv | uniq >'+config.get_ids_path+'pro_ids.csv'
        status = os.system(sentence)
        logger1.info('over get_ids.py')
        os.system('nohup python get_ProHtml.py &')
    except Exception,e:
        print e
        logger2.error(str(e))
        
        
