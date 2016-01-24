#!/usr/bin/env python
# encoding: utf-8

import signal

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.gen
import tornado.concurrent


from tornado import httpclient
from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

# 到底是什么构成了Future？
t = tornado.concurrent.Future()

def hello():
    print "hello"

def h(x, y):
    t.set_result("hello")

signal.signal(signal.SIGALRM, h)
# Set up a signal to repeat every 2 seconds
signal.setitimer(signal.ITIMER_REAL, 3, 0)


class MainHandler(tornado.web.RequestHandler):

    def call_me_maybe(self, result):
        self.write(result.body)
        self.finish()
        print("ok, the request has been closed")

    @tornado.web.asynchronous
    def get(self):
        # yield t
        httpclient.AsyncHTTPClient().fetch("http://baidu.com", callback=self.call_me_maybe) # fetch这个方法本身是如何运作的？
        print("i get called")
        # b = yield t
        # self.write(b.body)


def main():
    tornado.options.parse_command_line()

    tornado.netutil.Resolver.configure("tornado.netutil.ThreadedResolver")

    # TODO 疑问一，在我不用curl库的时候，默认的异步simple http client是如何做到高并发的？
    # httpclient.AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")

    application = tornado.web.Application([
        (r"/", MainHandler),],
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
