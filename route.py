#encoding=utf8
from scrapy import selector
import urllib2,re,json
from collections import OrderedDict

def getStatus():
    if len(urllib2.urlopen('http://127.0.0.1:2222/',timeout=2).read())>100: return "{'status':true}"
    return "{'status':false}"

def getScore(id):
    id=str(id)
    # if id[2]=='5': url = 'http://211.67.208.67/xxjw/xscjcx.jsp?yzbh='
    # else: url = 'http://211.67.208.69/kdjw/xscjcx.jsp?yzbh='
    error_return = "{'error':true}"
    if id[2]=='5': url = 'http://127.0.0.1:2222/xxjw/xscjcx.jsp?yzbh='
    else: url = 'http://127.0.0.1:2222/kdjw/xscjcx.jsp?yzbh='
    try:
        html=urllib2.urlopen(url+str(id),timeout=5).read()
        if len(html)<100 : return u"{'error':true,'msg':'内网服务器脱机'}"
        sel=selector.Selector(text=html)
    except Exception,e:
        print e
        return u"{'error':true,'msg':'服务器加载数据失败'}"
    table_heads=sel.xpath('//*[@id="xsjbxx"]/tr/td/text()').extract()
    name = table_heads[1]
    id = table_heads[3]
    idcard = table_heads[5]
    major = table_heads[9]
    _class = table_heads[11]
    college = table_heads[7]
    term=""
    every_score = []
    detail = OrderedDict()
    tr = sel.xpath('//*[@id="xscjxx"]/tr').extract()
    tr.append("colspan")
    for i in tr:
        if i.find(u"colspan")!=-1:
            if len(every_score)>1:
                detail[term]=every_score
                if i=='colspan':break
            every_score=[]
            try:
                term =  re.search('>.*<',i).group()[6:-1]
            except Exception,e:
                pass
        else :
            title,grade,score,Null = re.findall('(?<=\>).*(?=<)',i)
            item = {'title':title,'grade':grade,'score':score}
            every_score.append(item)
    js = OrderedDict({'name':name,'college':college,'major':major,'class':_class,'id':id,'idcard':idcard})
    js['detail'] = detail
    return json.dumps(js,ensure_ascii=False,indent=None,encoding='UTF8')

if __name__ == 'main':
    print s.encode('gbk','ignore')
