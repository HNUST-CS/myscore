#encoding=utf8
import sys
sys.path.append('server')
from flask import *
import flask
import route
import re
from werkzeug.contrib.cache import SimpleCache
import time
import os
import ipdb
app = Flask(__name__)
cache = SimpleCache()
# app.config['SEND_FILE_MAX_AGE_DEFAULT']=-1

import log
logger = log.getloger()

@app.route('/api/score/<int:id>/<idcard>')
def getScore(id,idcard):
    try:
        # ipdb.set_trace()
        return json.dumps(route.get_info_by_id(id,idcard.encode('utf8')),ensure_ascii=False)
    except Exception,e:
        logger.error('%s %s'%(id,e) )
        raise e
        return "{'error':true,'msg':'未知错误'}"

@app.route('/')
def index():
    # import ipdb;ipdb.set_trace()    
    return send_file('index.html')

if __name__ == '__main__':
    app.run(debug=True,use_debugger=True,host='0.0.0.0',port=3000)
    # app.run(debug=False,use_debugger=False,host='0.0.0.0',port=3000)

    

# getScore('120501027','432522199508263732')