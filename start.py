#-*-coding:utf-8-*-
import config,os,re
from myutil import httptools
from common import *
import logging
import logging.config

logging.config.fileConfig("./log/logging.conf")    # 采用配置文件  
logger1 = logging.getLogger("logger1")   
logger2 = logging.getLogger("logger2") 

listing=re.compile(r'<span class="rcnt|listingscnt"\s*>(.*?)</span>')
num_regx= re.compile('\d*,?\d*,?\d*')

def judge(input_num,lenth):
    if input_num=='':
        exit()
    input_num=int(input_num)
    if input_num in range(1,lenth+1):
        return 1
    else:
        return 0
def mkdir_folders():
    if os.path.exists(config.check_result_path+'process_record.txt')==1:
        os.remove(config.check_result_path+'process_record.txt')
    if os.path.exists(config.ope_path)==0:
        os.mkdir(config.ope_path)
    if os.path.exists(config.loc_path)==0:
        os.mkdir(config.loc_path)
    if os.path.exists(config.cate_path)==0:
        os.mkdir(config.cate_path)
    if os.path.exists(config.category_listings_path)==0:
        os.mkdir(config.category_listings_path)
    if os.path.exists(config.get_ids_path)==0:
        os.mkdir(config.get_ids_path)
    if os.path.exists(config.pro_html_path)==0:
        os.mkdir(config.pro_html_path)
    if os.path.exists(config.twsc_html_path)==0:
        os.mkdir(config.twsc_html_path)
    if os.path.exists(config.analy_path)==0:
        os.mkdir(config.analy_path)
    if os.path.exists(config.check_result_path)==0:
        os.mkdir(config.check_result_path)
    if os.path.exists(config.pro_html_file_path)==0:
        os.mkdir(config.pro_html_file_path)
    if os.path.exists(config.twsc_html_file_path)==0:
        os.mkdir(config.twsc_html_file_path)
def execute_program():
    print '1 execute program'
    print '2 back'
    num_input=raw_input('input number:')
    if judge(num_input,2)==0:
        print 'Input is not legal, please re-enter.'
        execute_program()
    if num_input=='1':
        mkdir_folders()
        os.system('nohup python get_leaf_cate_id.py &')
        print 'start running...'
    if num_input=='2':
        get_status()
        execute_program()
def get_status():
    print '1 get spot status'
    print '2 pass'
    num_input=raw_input('input number:')
    if judge(num_input,2)==0:
        print 'Input is not legal, please re-enter.'
        get_status()
    if num_input=='2':
        return
    tool=httptools.httptools()
    root_url=config.url.replace('[category]',config.root_category_id)
    listings=get_listings(tool,root_url)
    except_space=int(listings)*0.1745/1024
    left_space=get_left_space()
    print 'listings:',listings
    print 'excepted space:',str(int(except_space))+'G'
    print 'left space:',str(left_space)+'G'
    get_running_process()  
def modify_config(ope,loc,cate):
    f=open('config.py')
    lines=f.readlines()
    f.close()
    loc_num=config.location[loc]
    cate_id=config.category_dic[cate]
    lines[1]="root_name='"+cate+"'\n"
    lines[2]="root_category_id='"+cate_id+"'\n"
    lines[3]="loc='"+loc+"'"+'\n'
    lines[4]="ope='"+ope+"'"+'\n'
    lines[5]="url='http://www.ebay.com/sch/[category]/i.html?&LH_ItemCondition=3&LH_BIN=1&LH_RPA=1&LH_LocatedIn="+loc_num+"&_ipg=200&_pgn=1&_udlo=&_udhi=&_dmd=1'"+'\n'
    f=open('config.py','w')
    f.writelines(lines)
    f.flush()
    f.close()
    reload(config)
    command="sed -n '2,6p' config.py"
    lines=os.popen(command).read()
    print lines
def select_category():
    cate_dic=config.category_dic
    for i in range(1,13):
        print i,cate_dic.keys()[i-1]
    num_cate=raw_input('Select category:')
    if judge(num_cate,12):
        cate=cate_dic.keys()[int(num_cate)-1]
    else:
        print 'Input number is not legal, please re-enter.'
        select_category()
    return cate
def select_location():
    loc_list=['cn','us','hk']
    for i in range(len(loc_list)):
        print i+1,loc_list[i]
    loc_num=raw_input('Select location:')
    if judge(loc_num,len(loc_list)):
        loc=loc_list[int(loc_num)-1]
    else:
        print 'Input is not legal, please re-enter.'
        select_location()
    return loc  
def select_operation():
    ope_list=['get','update','add','get_status']
    for i in range(len(ope_list)):
        print i+1,ope_list[i]
    num_ope=raw_input('Select operation:')
    if judge(num_ope,len(ope_list)):
        ope=ope_list[int(num_ope)-1]
        if ope!='get_status':
            return ope
        else:
            print 'left disk space:',get_left_space()
            get_running_process()
            exit()
    else:
        print 'Input is not legal, please re-enter.'
        select_operation()     
"""
设置要抓取的品类，新建相应的文件夹。
"""
if __name__=='__main__':
    try:
        ope=select_operation()
        print ope
        loc=select_location()
        cate=select_category()
        print 'have selected:',ope,loc,cate
        logger1.info(ope+' '+loc+' '+cate)
        modify_config(ope,loc,cate)
        get_status()
        execute_program()        
    except Exception,e:
        print e
        logger2.error(str(e))
"""
还差：
'toys':'220',ssh jiping@52.23.251.215 
'home_garden':'11700',ssh jiping@54.175.102.79 
'clothing':'11450',
'video_games':'1249',ssh jiping@54.174.161.23
'computers':'58058',
"""
        
