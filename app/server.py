#!/usr/bin/env python

import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.locks
import tornado.options
import tornado.web
import os

from tornado.options import define, options

import paho.mqtt.client as mqtt

# Very useful:
# https://github.com/tornadoweb/tornado/blob/master/demos/blog/blog.py

define("port", default=8888, help="run on the given port", type=int)


class Application(tornado.web.Application):

    def __init__(self, mqtt_client):
        handlers = [
            (r"/", HomeHandler, dict(mqtt_client=mqtt_client)),
            (r"/entry/([^/]+)", EntryHandler),
        ]
        super(Application, self).__init__(handlers)


class BaseHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Jwt")
        self.set_header('Access-Control-Allow-Methods',
                        'POST, GET, OPTIONS, DELETE, PUT')
        self.set_header('Content-type', 'application/json')

    def options(self, params=None):
        self.finish()


class HomeHandler(BaseHandler):

    mqtt_client = None

    def initialize(self, mqtt_client):
        self.mqtt_client = mqtt_client

    async def get(self):
        self.mqtt_client.publish("hello/debug2")
        self.write('{"hello": "world"}')


class EntryHandler(BaseHandler):
    async def get(self, slug):
        self.write('{"hello": " ' + str(slug) + ' "}')


async def main():
    mqtt_client = mqtt.Client(client_id="sdasdjij")
    mqtt_client.username_pw_set(username="username", password="password")
    mqtt_client.connect(os.environ.get('MQTT_BROKER_ADDR', 'localhost'))
    mqtt_client.loop_start()

    tornado.options.parse_command_line()
    app = Application(mqtt_client)
    app.listen(options.port)

    # In this demo the server will simply run until interrupted
    # with Ctrl-C, but if you want to shut down more gracefully,
    # call shutdown_event.set().
    shutdown_event = tornado.locks.Event()
    await shutdown_event.wait()


if __name__ == "__main__":
    tornado.ioloop.IOLoop.current().run_sync(main)