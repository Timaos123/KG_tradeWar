# -*- coding=utf-8 -*-
# name: tornado web server
# author: humanman
# date: 2016-08-10

# import json,pickle,time,re,Levenshtein,base64,datetime,random
import os.path
import os
import requests
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options, parse_command_line

define("port", default=8888, help="run on the given port", type=int)

from acupuncture_handlers_search import *

class MakeApp(tornado.web.Application):
    def __init__(self):
        handlers = [

            (r"/AD", ADHandler),
            (r"/.*", BaseHandler)

        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret='61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=',
            login_url='/xuewei/login',
        )
        super(MakeApp, self).__init__(handlers, **settings)


class SideHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("side.html")

class FooterHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("footer.html")

class BaseHandler(tornado.web.RequestHandler):
    def get(self):
        self.write_error(404)
    def write_error(self, status_code, **kwargs):
        self.write('error:' + str(status_code))

def main():
    parse_command_line()
    app = MakeApp()
    print("search 127.0.0.1:8888/AD")
    app.listen(options.port, address="0.0.0.0")
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()