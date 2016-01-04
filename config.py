#-*-coding:utf-8-*-
root_name='home_garden'
root_category_id='11700'
loc='us'
ope='get'
url='http://www.ebay.com/sch/[category]/i.html?&LH_ItemCondition=3&LH_BIN=1&LH_RPA=1&LH_LocatedIn=1&_ipg=200&_pgn=1&_udlo=&_udhi=&_dmd=1'
location={'cn':'45','us':'1','hk':'92'}
category_dic={'toys':'220',
            'outdoors':'159043',
            'jewelry':'281',
            'cell_phone':'15032',
            'pets':'1281',
            'camera':'625',
            'home_garden':'11700',
            'clothing':'11450',
            'office':'25298',
            'computers':'58058',
            'video_games':'1249',
            'consumer_elec':'293'}
ope_path='./result/'+ope
loc_path=ope_path+'/'+loc
cate_path=loc_path+'/'+root_name
category_listings_path=cate_path+'/get_category_listings/'
get_ids_path=cate_path+'/get_ids/'
pro_html_path=cate_path+'/get_pro_html/'
pro_html_file_path=pro_html_path+root_name+'_ProHtmlFile/'
twsc_html_path=cate_path+'/get_twsc_html/'
twsc_html_file_path=twsc_html_path+root_name+'_TwscHtmlFile/'
analy_path=cate_path+'/analyze_result/'
check_result_path=cate_path+'/check_result/'

each_category='./source/each_category.txt'








