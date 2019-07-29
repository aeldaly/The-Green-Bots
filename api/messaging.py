import zmq
import json
import argparse
import tornado.httpserver
import tornado.ioloop
from tornado import web
from tornado.options import define, options
from server import BaseHandler


class SubscriptionHandler(BaseHandler):
    def get(self):
        self.write(json.dumps())

    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        print(data)


class PublisherHandler(BaseHandler):
    def get(self):
        self.write(json.dumps())

    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        print(data)


class MessagesHandler(BaseHandler):
    def get(self):
        self.write(json.dumps())

    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        print(data)


class Reactor:
    def __init__(self):
        self.topic_to_callback = {}
        self.sub_context = zmq.Context()
        self.sub = self.sub_context.socket(zmq.SUB)
        self.sub.connect('tcp://0.0.0.0:9900')
        self.sub.setsockopt(zmq.LINGER, 0)    # discard unsent messages on close
        self.pub_context = zmq.Context()
        self.pub = self.pub_context.socket(zmq.PUB)
        self.pub.bind("tcp://0.0.0.0:9900")

    def subscribe(self, topic, callback):
        self.topic_to_callback[topic] = dict(callback=callback)
        self.sub.setsockopt(zmq.SUBSCRIBE, topic)

    def publish(self, topic, message):
        self.pub.send("%d %d" % (topic, message))

    def spin(self):
        while True:
            data = self.sub.recv()
            topic, message = data.split()
            self.topic_to_callback[topic]['callback'](message)


class Application(web.Application):
    def __init__(self, topic_to_callback):
        self.topic_to_callback = topic_to_callback
        handlers = [
            (r"/api/messages/subscribe/", SubscriptionHandler),
            (r"/api/messages/publish/", PublisherHandler),
            (r"/api/messages/", MessagesHandler),
        ]
        web.Application.__init__(self, handlers)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Web Interface api')
    parser.add_argument('--port', type=int, help="port to run on. Must be supplied.")
    args = parser.parse_args()
    define("port", default=args.port, help="Run on the given port", type=int)
    http_api = tornado.httpserver.HTTPServer(Application(
        topic_to_callback=dict()
    ))
    http_api.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
