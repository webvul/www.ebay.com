#coding:utf-8
import re
import os, sys
#import MySQLdb
from settings import DATABASES as dbconfig
""" 
    @param 无
    @note 创建数据库连接
    @return 连接对象 connection
    @author lvhao
    @date 2015-04-27
"""
def get_conn():    
    DATABASES = dbconfig['default']
    conn = MySQLdb.Connect(host=DATABASES['HOST'], user=DATABASES['USER'], local_infile=1,
                           passwd=DATABASES['PASSWORD'], db=DATABASES['NAME'], charset="utf8")
    return conn  


""" 
    @param
         sql：sql语句 
    @note 根据给出的sql插入数据
    @return 无
    @author lvhao
    @date 2015-04-27
"""
def insert_data(sql):
    try:
        print sql
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
    except Exception,e:
        print e
""" 
    @param 
        cat_id：品类id 
    @note 根据品类id查询此品类是否存在
    @return 存在返回1，不存在返回0
    @author lvhao
    @date 2015-04-27
"""
def get_cat_data(cat_id):
    conn = get_conn()
    cur = conn.cursor()
    re = cur.execute('select 1 from EA.pro_db_models_category where category_id='+cat_id)
    cur.close()
    conn.close()
    return re
""" 
    @param 
        seller_name：卖家名称
        seller_url：卖家链接
        feadback_score：信用得分
        good_rate：好评率
        location：卖家位置
    @note 根据给出的参数，拼接EA.market_selle表的insert语句
    @return sql语句
    @author lvhao
    @date 2015-04-27
"""
def get_add_seller_sql(seller_name,seller_url,feadback_score,good_rate,location):
    if feadback_score is None:
        feadback_score = '0'
    elif feadback_score == '':
        feadback_score = '0'
    sql = 'insert into EA.market_seller values(null,"'+seller_name+'","'+seller_name+'",'
    sql = sql + '"'+seller_url+'",1,null,'+feadback_score+',"'+good_rate+'","'+location+'")'
    return sql
""" 
    @param 
        seller_id：卖家名称
    @note 根据卖家名称查询此卖家是否存在
    @return 存在返回1，不存在返回0
    @author lvhao
    @date 2015-04-27
"""
def get_seller_data(seller_id):
    conn = get_conn()
    cur = conn.cursor()
    re = cur.execute('select 1 from EA.market_seller where seller_id="'+seller_id+'"')
    cur.close()
    conn.close()
    return re
""" 
    @param 
        seller_id：卖家名称
        ids: 完整品类的id
    @note 根据卖家名称查询此卖家和品类的关系是否存在
    @return 存在返回1，不存在返回0
    @author lvhao
    @date 2015-05-06
"""
def get_seller_cate(seller_id,ids):
    conn = get_conn()
    cur = conn.cursor()
    re = cur.execute('select 1 from EA.pro_db_models_sellercategory where seller_id="'+seller_id+'" and category_id="'+ids+'"')
    cur.close()
    conn.close()
    return re

def get_product(item_id,variation_id):
    conn = get_conn()
    cur = conn.cursor()
    re = cur.execute('select 1 from EA.pro_db_models_marketproducts where product_id="'+item_id+'" and variationId="'+variation_id+'"')
    cur.close()
    conn.close()
    return re
""" 
    @param 
        seller_id：卖家名称
        category_id：品类id
    @note 根据给出参数，拼接EA.pro_db_models_sellercategory（seller和category的映射关系表）的insert语句
    @return sql语句
    @author lvhao
    @date 2015-04-27
"""
def get_add_cat_seller_data_sql(seller_id, category_id):
    #sid = '(select id from EA.market_seller where seller_id="'+seller_id+'")'
    #cid = '(select id from EA.pro_db_models_category where category_id='+str(category_id)+')'
    return 'insert into EA.pro_db_models_sellercategory values(null,"'+seller_id+'","'+category_id+'")'





def get_add_info_sql(infos):
    sql = ''
    if infos:
        variation_id = infos[0]
        item_id = infos[3]
        brand = infos[1].replace('"','')
        seller = infos[2]
        title = infos[4].replace('"','').replace('\'','').strip()
        title_key = __get_title_key(title)
        category_ids = infos[5]
        cates = category_ids[1:len(category_ids)-1].split('/')
        cate_one = 'null'
        cate_two = 'null'
        cate_three = 'null'
        cate_four = 'null'
        cate_five = 'null'
        cate_six = 'null'
        try:
            cate_one = cates[0]
            cate_two = cates[1]
            cate_three = cates[2]
            cate_four = cates[3]
            cate_five=cates[4]
            cate_six=cate[5]
        except:
            pass
        category_names = infos[6]
        available = infos[7]
        sell_count = infos[9]
        reviews = infos[10]
        item_price = infos[11]
        ship_price = infos[12]
        location = infos[13]
        craw_date = infos[14]
        good_rate = infos[15]
        standard_price = infos[16]
        seller_url = infos[17]
        description = infos[18]
        item_weight = infos[19]    
        drop_down_size = infos[20]
        drop_down_color = infos[21]    
        url = 'http://www.ebay.com/itm/'+str(item_id)
        currency = infos[11]
        try:
            regex = re.compile(r'\d*\.\d*',re.S)
            item_price_info = item_price.split(' ')
            item_price = regex.search(item_price_info[1].replace(',', '')).group()
            is_price = re.compile(r'^\d*\.\d*$',re.S).search(item_price_info[1].replace(',', ''))
            if is_price:
                currency = item_price_info[0]
            else:
                currency = item_price_info[1][0]
            ship_price = regex.search(ship_price).group()
        except Exception, e:
            pass
        try:
            sql = 'insert into EA.pro_db_models_marketproducts(title_key,product_id,title,product_url,market_id,market_name,brand_name,seller_id,seller_name,currency,'
            sql = sql + 'item_price,ship_price,available,sell_count,reviews,location,status,create_date,category_ids,category_names,good_rate,standard_price,'
            sql = sql + 'feature1,feature2,feature3,feature4,feature5,MainImage,OtherImage1,OtherImage2,OtherImage3,OtherImage4,OtherImage5,OtherImage6,OtherImage7,OtherImage8,'
            sql = sql + 'variationId,category_one_id,category_two_id,category_three_id,category_four_id,category_five_id,category_six_id,seller_url,'
            sql = sql + 'description,weight,size_drop_down,color_drop_down) values("'
            sql = sql + str(title_key) + '","' + str(item_id) + '",\''+title+'\',"'+url+'",1,"ebay","'+brand+'","'+seller+'","'+seller+'","'+currency+'","'+item_price+'","'
            sql = sql + ship_price + '","'+available+'","'+sell_count+'","'+reviews+'","'+location+'",0,"'+craw_date+'","'+category_ids+'","'+category_names+'","'+good_rate+'","'+standard_price+'","'
            sql = sql + infos[22] + '","' + infos[23] + '","' + infos[24] + '","' + infos[25] + '","' + infos[26] + '","' + infos[27] + '","' + infos[28] + '","' 
            sql = sql + infos[29] + '","' + infos[30] + '","' + infos[31] + '","' + infos[32] + '","' + infos[33] + '","' + infos[34] + '","' + infos[35] + '","'
            sql = sql +variation_id+'",'+cate_one+','+cate_two+','+cate_three+','+cate_four+','+cate_five+','+cate_six+',"'+seller_url+'","'
            sql = sql +'","'+item_weight+'","'+drop_down_size+'","'+drop_down_color+'")'
        except Exception,e:
            print e
    return sql

def __get_title_key(title):
    title_words = title.split(' ')
    if title_words[0] == 'The':
        return title_words[1]
    else:
        return title_words[0]


def get_pro_id_title(cate_one,count):
    sql = 'select product_id,title from EA.pro_db_models_marketproducts where category_one_id='+str(cate_one)+' limit '+str(count)+',1000'
    print sql
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql)
    produncts = cur.fetchall()
    pro_list = []
    for item in produncts:
        pro_dic={'product_id':'','title':''}
        pro_dic['product_id'] = str(item[0])
        pro_dic['title'] = item[1]
        pro_list.append(pro_dic)
    cur.close()
    conn.close()
    return pro_list


def get_new_product_sql(infos):
    file_title = ["variationId","brand_id","Seller_id","product_ID", "Title", "category_ids", "category_names","avalible","Seller_Score","sell_count", "Reviews","item_Price","ship_price","Location","create_date","feature1","feature2", "feature3","feature4","feature5", "MainImage","OtherImage1","OtherImage2","OtherImage3","OtherImage4", "OtherImage5","OtherImage6","OtherImage7", "OtherImage8","Variation_map", "location_code","status"]
    sql = 'insert into models_products values'



