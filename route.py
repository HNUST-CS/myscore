from scrapy import selector
import urllib2,re,json
from collections import OrderedDict
def getScore(id):
    id=str(id)
    if id[2]=='5': url = 'http://211.67.208.67/xxjw/xscjcx.jsp?yzbh='
    else: url = 'http://211.67.208.69/kdjw/xscjcx.jsp?yzbh='
    try:
        sel=selector.Selector(text=urllib2.urlopen(url+str(id)).read())
    except:
        return "{'error':true}"
    # import ipdb;ipdb.set_trace()    
    table_heads=sel.xpath('//*[@id="xsjbxx"]/tr/td/text()').extract()
    print table_heads
    name = table_heads[1]
    id = table_heads[3]
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
                term =  re.search('>.+<',i).group()[6:-1]
            except Exception,e:
                pass
        else :
            title,grade,score,Null = re.findall('(?<=\>).+(?=<)',i)
            item = {'title':title,'grade':grade,'score':score}
            every_score.append(item)
    js = {'name':name,'college':college,'major':major,'class':_class,'id':id,'detail':detail}
    return json.dumps(js,ensure_ascii=False,indent=None,encoding='UTF8')

if __name__ == 'main':
    print s.encode('gbk','ignore')
