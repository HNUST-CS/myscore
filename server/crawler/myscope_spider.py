#encoding=utf8
import re
import json
import datetime
import htmlToJson
from scrapy.selector import Selector
try:
    from scrapy.spider import Spider
except:
    from scrapy.spider import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle


import sys
reload(sys)
sys.setdefaultencoding('utf-8')




import pymongo
MYSCOPE_DB = pymongo.Connection().myscope.all
# import ipdb;ipdb.set_trace()

class myscopeSpider3(CrawlSpider):
    name = "myscope"
    allowed_domains = ["*"]

    def trans_url(id):
        if id[2]=='5': return 'http://211.67.208.67/xxjw/xscjcx.jsp?yzbh='+id
        else: return 'http://211.67.208.69/kdjw/xscjcx.jsp?yzbh='+id

    start_urls = [trans_url(id) for id in open("id_list.txt").read().split()]
    # print start_urls
    def parse(self,response):
        url = response.url
        html = response.body_as_unicode()
        try:
            js = htmlToJson.htmlToJson(html)
            MYSCOPE_DB.save(js)
        except :
            pass




