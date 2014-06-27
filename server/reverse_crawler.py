#encoding=utf8

import ipdb;

base_url = 'http://kdjw.hnust.cn'

def pre():
    import urllib2, cookielib,urllib,re
    cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)

    url_index = base_url+'/kdjw/'
    url_img = base_url+'/kdjw/verifycode.servlet'

    ipdb.set_trace()
    opener.open(url_index).read()
    img_date = opener.open(url_img).read()
    open('a.jpg','wb').write(img_date)
    cookie = cookie_support.cookiejar._cookies
    return cookie

def cha(id,cookie,code):
    import urllib2, cookielib,urllib,re
    cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())
    cookie_support.cookiejar._cookies = cookie
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    name,idcard = id_name(id)

    url_submit = base_url+'/kdjw/xscjcx_check.jsp'
    postdata=urllib.urlencode({
        'xsxm':name.encode('utf8'),
        'xssfzh':idcard,
        'yzm':code,
    })

    res = opener.open(url_submit,postdata).read()
    if 'yzm_guoq' in res : print '验证码过期' ; return ;
    url_scope = base_url+'/kdjw/xscjcx.jsp?yzbh=' + res[-36:-4]
    html = opener.open(url_scope).read()
    print html
    if not re.search('\d{10}',html) : print '查询失败'


def id_name(id):
        import pymongo
        db = pymongo.Connection().myscope.all
        r = db.find_one({'id':'1205010207'},{'name':1,'idcard':1})
        return r['name'],r['idcard']


cookie = pre()

