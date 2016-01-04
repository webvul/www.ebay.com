#-*-coding:UTF-8-*-
import config,re,os
from multiprocessing import Pool,Lock
from myutil import httptools
import logging
import logging.config
import chardet


logging.config.fileConfig("./log/logging.conf")    # 采用配置文件  
logger1 = logging.getLogger("logger1")   
logger2 = logging.getLogger("logger2") 

regex_child = re.compile(r'<div class="cat-link">(.*?)</a>')
regex_cate_id = re.compile(r'sch/.*?/(.*?)/')

regex_root_cate_info = re.compile(r"<li itemprop='itemListElement'(.*?)</li>",re.S)
regex_root_cate_id = re.compile(r'<a href=.*?/sch/.*?/(.*?)/')

def get_root_cate_id(html):
    cate_info = regex_root_cate_info.search(html)
    if cate_info != None:
        cate_info = cate_info.group(1)
        cate_id = regex_root_cate_id.search(cate_info)
        if cate_id != None:
            cate_id = cate_id.group(1)
        return cate_id
    else:
        return

def get_current_page_info(cate_id):#若没有子品类，返回[]；否则返回子品类列表
    url = config.url.replace('[category]',cate_id)
    for i in range(3):
        html = tool.gethtml(url)
        if html.find('We were unable to run the search you entered. Please try again in a few minutes.') == -1:
            break
    if html.find('We were unable to run the search you entered. Please try again in a few minutes.') != -1:
        logger2.error(cate_id+'\t'+'We were unable to run the search you entered. Please try again in a few minutes.')
        return
    
    if html.find('<div class="catsgroup leafsiblings">') != -1:#leaf品类
        root_id = get_root_cate_id(html)
        if str(root_id) != config.root_category_id:
            logger2.error(str(root_id)+'\t'+'该品类不属于一级品类')
            return
        lock.acquire()
        f.write(cate_id+'\n')
        f.flush()
        lock.release()
        return
    
    cate_list = []
    info_list = regex_child.findall(html)
    for child in info_list:
        cate_id = regex_cate_id.search(child)
        if cate_id != None:
            cate_id = cate_id.group(1)
        cate_list.append(cate_id)
    return cate_list

def get_leaf_cate_id(cate_id):
    cate_list = get_current_page_info(cate_id)
    if cate_list != None:
        for cate in cate_list:
            get_leaf_cate_id(cate)

def handle():
    global tool,f,lock
    tool = httptools.httptools()
    lock = Lock()
    path = config.category_listings_path+'leaf_cate_id.csv'
    f = open(path,'w')
    
    root_id = config.root_category_id
    cate_list = get_current_page_info(root_id)    
    
    pool = Pool(15)
    pool.map(get_leaf_cate_id,cate_list)
    pool.close()
    pool.join()

    f.close()  

"""
获取该一级品类下所有leaf_cate_id
"""
if __name__ == '__main__':
    logger1.info('get_leaf_cate_id.py start...')
    handle()
    logger1.info('get_leaf_cate_id.py over')
    os.system('nohup python get_category_listings.py &')
