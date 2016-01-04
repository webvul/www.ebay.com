#/usr/bin/env python
#-*-coding:utf-8-*-
from multiprocessing import Pool,Lock
from myutil import httptools
import config
import os,re
import logging
import logging.config

logging.config.fileConfig("./log/logging.conf")    # 采用配置文件  
logger1 = logging.getLogger("logger1")   
logger2 = logging.getLogger("logger2") 
    
def get_product_html(line):
    try:
        id=line.strip()
        url="http://www.ebay.com/itm/"+id
        html=tool.gethtml(url)
        if html.find('<urlopen error [Errno -2] Name or service not known>')!=-1:
            logger2.warning(id+'\t'+'<urlopen error [Errno -2] Name or service not known>')
            return
            
        lock.acquire() 
        f=open(config.pro_html_file_path+id+'.html','w')
        f.write(html)
        f.flush()
        f.close()
        success_file.write(id+'\n')
        success_file.flush()
        lock.release() 
    except Exception,e:
        logger2.error(id+'\t'+str(e))    

def handle():
    global lock,tool,success_file
    tool=httptools.httptools()
    lock=Lock()
    success_file = open(config.pro_html_path+'ids_FromProHtml.txt','aw')

    path = config.get_ids_path+'pro_ids.csv'
    f1=open(path)
    while True:#为了减少内存使用，每次只读取10000行进行抓取
        lines = []
        for i in range(10000):
            line=f1.readline()
            if not line:
                break
            lines.append(line)
        if lines ==[]:
            break
        pool=Pool(10)
        pool.map(get_product_html,lines)
        pool.close()
        pool.join()
        
        if not line:
            break
    f1.close()
    
    success_file.close()

def write_ids(names):#把product_id写入文件
    if names == []:
        return
    f=open(config.pro_html_path+'ids_FromProHtml.txt','w')
    for name in names:
        id=name.replace('.html','')
        f.write(id+'\n')
        f.flush()
    f.close()

def judge_break():
    try:
        names=os.listdir(config.pro_html_file_path)
        if len(names) < 1000:#若抓取的页面小于1000，则重新抓取；若大于1000，取剩余的id，再进行抓取。
            write_ids(names)
            return
        write_ids(names)
        del names#释放内存，使得下一步取差集更顺利。
        
        path_pro_ids = config.get_ids_path+'pro_ids.csv'#取差集
        path_html_ids = config.pro_html_path+'ids_FromProHtml.txt'
        command1 = 'sort %s %s |uniq -u > chaji.csv' % (path_pro_ids,path_html_ids)
        command2 = 'mv chaji.csv %s' % path_pro_ids
        status = os.system(command1)
        if status == 0:
            os.system(command2)
    except Exception,e:
        logger2.error(str(e))

if __name__=='__main__':
    try:
        logger1.info('start get_ProHtml.py...')
        judge_break()
        handle()
        names=os.listdir(config.pro_html_file_path)
        write_ids(names)
        logger1.info('over get_ProHtml.py')
    except Exception,e:
        logger2.error(str(e))
"""
平均 76924个id/M 100万个id=12.9M
思路：
1)是否已经抓取了一些html文件。
    若无，直接抓取
    若小于1000，重新抓取，并把已经抓取到id写入，ids_FromProHtml.txt中。
    若大于1000，则取出尚未抓取的id进行抓取。。
2）读取一万个id，抓取html文件。然后循环该动作。已经获取到html的id，写入 ids_FromProHtml.txt 
3）获取已经抓取的html文件的id。
"""
