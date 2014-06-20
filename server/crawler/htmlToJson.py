#encoding=utf8
from scrapy import selector
import urllib2,re,json,datetime
from collections import OrderedDict

def htmlToJson(html):
    sel=selector.Selector(text=html)
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
    js = OrderedDict({'name':name,'college':college,'major':major,'class':_class,'id':id,'idcard':idcard,'datetime':datetime.datetime.now()})
    js['detail'] = detail
    return js

