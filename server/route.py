#encoding=utf8
from collections import OrderedDict
from scrapy import selector
import urllib2, cookielib,urllib,re,json,sys,datetime,base64,time
import ipdb,requests

sys.path.append('server/crawler')
sys.path.append('crawler')
import pymongo
MYSCOPE_DB = pymongo.Connection().myscope.all
import htmlToJson

def getStatus():
    if len(urllib2.urlopen('http://127.0.0.1:2222/',timeout=2).read())>100: return "{'status':true}"
    return "{'status':false}"


def getScore(id):
    id=str(id)
    dic = MYSCOPE_DB.find_one({'id':id},{'_id':0})
    if not dic : return "{'status':false}"
    # if  (datetime.datetime.now()-dic['datetime']).total_seconds() > 24*3600 : return getScoreByWeb(id)
    dic['from'] = 'mongodb'
    dic['datetime'] = dic['datetime'].isoformat()
    return json.dumps(dic,ensure_ascii=False,indent=None,encoding='UTF8')


def getScoreByWeb(id):
    id=str(id)
    # if id[2]=='5': url = 'http://211.67.208.67/xxjw/xscjcx.jsp?yzbh='
    # else: url = 'http://211.67.208.69/kdjw/xscjcx.jsp?yzbh='
    if id[2]=='5' or id[2]=='6': url = 'http://127.0.0.1:2222/xxjw/xscjcx.jsp?yzbh='
    else: url = 'http://127.0.0.1:2222/kdjw/xscjcx.jsp?yzbh='
    try:
        html=urllib2.urlopen(url+str(id),timeout=5).read()
        if len(html)<100 : return u"{'error':true,'msg':'内网服务器脱机'}"
    except Exception,e:
        return u"{'error':true,'msg':'服务器加载数据失败'}"

    dic = htmlToJson.htmlToJson(html)
    MYSCOPE_DB.save(dic)
    del dic['_id']
    dic['from'] = 'web'
    dic['datetime'] = dic['datetime'].isoformat()
    return json.dumps(dic,ensure_ascii=False,indent=None,encoding='UTF8')


def get_session(kind):
    if kind == 'xxjw' : base_url = 'http://xxjw.hnust.cn/xxjw'
    elif kind == 'kdjw' : base_url = 'http://kdjw.hnust.cn/kdjw'
    else : return {'error':True,'msg':"填写有误"}
    opener = requests.Session()
    url_img = base_url+'/verifycode.servlet'
    try :
        opener.get(base_url)
        img = opener.get(url_img)
        img_date = img.content
        open('a.jpg','wb').write(img_date)
    except :
        return {'error':True,'msg':"请求失败，内网服务器脱机，请稍后再试或者联系我们。"}
    img_base64 = base64.encodestring(img_date)
    return json.dumps({'cookie':opener.cookies.get_dict(),'img':img_base64})


def id_name(id):
    r = MYSCOPE_DB.find_one({'id':'1205010207'},{'name':1,'idcard':1})
    return r['name'],r['idcard']

def verify(id,idcard):
    r = MYSCOPE_DB.find_one({'id':'1205010207'},{'name':1,'idcard':1})
    if r['idcard'][-4:] == idcard : return True
    return False

def cha(id,idcard,cookie,code):
    print cookie
    opener = requests.Session()
    opener.cookies.set('JSESSIONID',cookie[15:56])
    ipdb.set_trace()
    if not verify(id,idcard) : return {'error':True,'msg':"身份证号码错误"}
    try: name,idcard = id_name(id)
    except : return {'error':True,'msg':"未找到您输入信息的学生"}
    if int(id[2])>3: kind = 'xxjw'
    else : kind = 'kdjw'
    if kind == 'xxjw' : base_url = 'http://xxjw.hnust.cn/xxjw'
    elif kind == 'kdjw' : base_url = 'http://kdjw.hnust.cn/kdjw'
    else : return {'error':True,'msg':"填写有误"}
    
    url_submit = base_url+'/xscjcx_check.jsp'

    opener = requests.Session()
    payload = {
        'xsxm':name.encode('utf8'),
        'xssfzh':idcard,
        'yzm':code,
    }

    res = opener.post(url_submit,payload).text
    if 'yzm_guoq' in res : return {'error':True,'msg':"验证码过期"}
    if 'yzm_cuowu' in res : return {'error':True,'msg':"验证码输入错误"}
    if 'notQueryXs' in res : return {'error':True,'msg':"未找到您输入信息的学生"}
    if 'systemError' in res : return {'error':True,'msg':"您访问的功能出现错误"}
    
    url_scope = base_url+'/xscjcx.jsp?yzbh=' + res[-36:-4]
    html = opener.open(url_scope).read()
    if not re.search('\d{10}',html) : return {'error':True,'msg':"查询失败"}
    return htmlToJson.htmlToJson(html)


if __name__ == 'main':
    print s.encode('gbk','ignore')

cookie = str(eval(get_session('kdjw') )['cookie'])
print cookie

def cha2(code):
    print cha('1205010207','3732',cookie,code)

