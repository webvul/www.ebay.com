#-*-coding:utf-8-*-
import config
import datetime
import time,os
from email.mime.multipart import MIMEMultipart
import smtplib
import logging  
import logging.config 

logging.config.fileConfig("./log/logging.conf")    # 采用配置文件  
logger1 = logging.getLogger("logger1")   
logger2 = logging.getLogger("logger2") 
# 
# def sleep_time():#每天四点开始执行抓取程序
#     t1=datetime.datetime.now()
#     t2=t1.replace(hour=8,minute=30,second=00)#设定每天开始抓取的抓取时间
#     t3=t2-t1
#     if t3.days==-1:
#         t_exe=t2+datetime.timedelta(days=1)
#     else:
#         t_exe=t2
#     t_sleep=(t_exe-t1).seconds
#     print '本次执行完时间：',t1
#     print '下次执行时间：',t_exe
#     print '睡眠时间：',t_sleep
#     return t_sleep  
# 
# def email_start():
#     msg = MIMEMultipart()
#     #加邮件头
#     to_list=['1121403085@qq.com']#发送给相关人员
#     msg['to'] = ';'.join(to_list)
#     msg['from'] = 'jiping@starmerx.com'
#     msg['subject'] = '开始抓取'
#     #发送邮件
#     try:
#         server = smtplib.SMTP()
#         server.connect('smtp.exmail.qq.com')
#         server.login('jiping@starmerx.com','ljp185')#XXX为用户名，XXXXX为密码
#         server.sendmail(msg['from'], to_list,msg.as_string())
#         server.quit()
#         print '发送成功'
#     except Exception, e:  
#         print '发送失败',e
#         logger2.error(str(e))

def get_progress(path):
    if os.path.exists(path):
        command = 'wc -l %s' % path
        row = os.popen(command).read()
        row = row.split(' ')[0]
        return row
    else:
        return

if __name__=='__main__':
    path1 = config.get_ids_path+'pro_ids.csv'
    row1 = get_progress(path1)
    print '所有id：',row1
    path2 = config.pro_html_path+'ids_FromProHtml.txt'
    row2 = get_progress(path2)    
    print '已经抓取id：',row2
    if row1 != None and row2 != None:
        print '抓取进度：',float(row2)/float(row1)