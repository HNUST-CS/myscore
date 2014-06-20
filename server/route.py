#encoding=utf8
from scrapy import selector
import urllib2,re,json
from collections import OrderedDict
import sys,datetime
sys.path.append('server/crawler')
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
    if  (datetime.datetime.now()-dic['datetime']).total_seconds() > 24*3600 : return getScoreByWeb(id)
    dic['from'] = 'mongodb'
    dic['datetime'] = dic['datetime'].isoformat()
    return json.dumps(dic,ensure_ascii=False,indent=None,encoding='UTF8')


def getScoreByWeb(id):
    id=str(id)
    # if id[2]=='5': url = 'http://211.67.208.67/xxjw/xscjcx.jsp?yzbh='
    # else: url = 'http://211.67.208.69/kdjw/xscjcx.jsp?yzbh='
    if id[2]=='5': url = 'http://127.0.0.1:2222/xxjw/xscjcx.jsp?yzbh='
    else: url = 'http://127.0.0.1:2222/kdjw/xscjcx.jsp?yzbh='
    try:
        html=urllib2.urlopen(url+str(id),timeout=5).read()
        if len(html)<100 : return u"{'error':true,'msg':'内网服务器脱机'}"
    except Exception,e:
        return u"{'error':true,'msg':'服务器加载数据失败'}"

    dic = htmlToJson.htmlToJson(html)
    import pdb;pdb.set_trace()    
    MYSCOPE_DB.save(dic)
    del dic['_id']
    dic['from'] = 'web'
    dic['datetime'] = dic['datetime'].isoformat()
    return json.dumps(dic,ensure_ascii=False,indent=None,encoding='UTF8')



if __name__ == 'main':
    print s.encode('gbk','ignore')
