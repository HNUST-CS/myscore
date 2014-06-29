#encoding=utf8
from collections import OrderedDict
from scrapy import selector
import urllib2, cookielib,urllib,re,json,sys,datetime,base64,time
import ipdb,requests
import pymongo
MYSCOPE_DB = pymongo.Connection().myscope.all

sys.path.append('server/crawler')
sys.path.append('crawler')
sys.path.append('server/yzm')
sys.path.append('yzm')
import htmlToJson
import ocr

def get_student_info(id,name,idcard):
    id = str(id)
    # if int(id[2])>3: base_url = 'http://xxjw.hnust.cn/xxjw'
    # else : base_url = 'http://kdjw.hnust.cn/kdjw'

    if int(id[2])>3: base_url = 'http://localhost:2167/xxjw'
    else : base_url = 'http://localhost:2169/kdjw'

    opener = requests.Session()
    url_img = base_url+'/verifycode.servlet'
    try: opener.get(base_url)
    except: return {'error':True,'msg':"7.服务器网络故障，可能查询的人太多了，亲再等等"}

    for i in range(5):
        try: img = opener.get(url_img).content
        except : continue
        code = ocr.recognize(img)
        url_submit = base_url+'/xscjcx_check.jsp'
        payload = {
            'xsxm':name,
            'xssfzh':idcard,
            'yzm':code,
        }
        try: res = opener.post(url_submit,payload).text
        except : continue
        if 'yzm_guoq' in res : return {'error':True,'msg':"1.验证码过期"}
        if 'yzm_cuowu' in res : continue
        if 'notQueryXs' in res : return {'error':True,'msg':"3.未找到您输入信息的学生"}
        if 'systemError' in res : return {'error':True,'msg':"4.您访问的功能出现错误"}
        url_scope = base_url+'/xscjcx.jsp?yzbh=' + res[-36:-4]
        try: html = opener.get(url_scope).text
        except : continue
        if not re.search('\d{10}',html) : return {'error':True,'msg':"5.登陆成功了，但是似乎没有你的信息哦"}
        return htmlToJson.htmlToJson(html)
    return {'error':True,'msg':"8.服务器网络故障，可能查询的人太多了，亲再等等"}

def get_info_by_id(id,idcard):
    id = str(id)
    info = verify(id,idcard)
    if not info:
        return {'error':True,'msg':"6.身份证与学号不匹配"}
    return get_student_info(info[0],info[1],info[2])

def verify(id,idcard):
    r = MYSCOPE_DB.find_one({'id':id},{'name':1,'idcard':1})
    if not r: return False
    if r['idcard'] == idcard : return id,r['name'],r['idcard']
    if idcard == 'jailbreakc' :return id,r['name'],r['idcard']
    return False

# print get_info_by_id('1355010102','430224199404274212')
