from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import sys
sys.path.append('server')
from app import app

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(3000)
IOLoop.instance().start()
