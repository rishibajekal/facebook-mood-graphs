import os
import pickle
import logging
import tornado.httpserver
import tornado.ioloop
import tornado.web
import pymongo
import sys
from tornado.options import options, define
from handlers.pages import *
from handlers.auth import *
from handlers.api import *

PORT = sys.argv[1]

LOCAL = True if (sys.argv[2] == '1') else False

define("port", default=PORT, help="run on the given port", type=int)
define("local", default=LOCAL, help="run on the given port", type=bool)
define("debug", default=True, help="run tornado in debug mode", type=bool)
MONGOHQ_URL = "mongodb://heroku:9ac7baaa86707047fc32970d185a71fd@alex.mongohq.com:10003/app8933198"


class Application(tornado.web.Application):
    def __init__(self):

        if LOCAL:
            conn = pymongo.connection.Connection()
            self.db = conn['sentipede']
        else:
            conn = Connection(MONGOHQ_URL)
            self.db = conn[urlparse(MONGO_URL).path[1:]]

        classifier_bin = open('static/resources/classifier.bin')
        self.classifier = pickle.load(classifier_bin)

        handlers = [
            # Page Handlers
            tornado.web.URLSpec(r'/', IndexPageHandler),
            tornado.web.URLSpec(r'/timeline', TimelinePageHandler),
            tornado.web.URLSpec(r'/location', LocationPageHandler),
            tornado.web.URLSpec(r'/likes', LikesPageHandler),

            # API Handlers
            tornado.web.URLSpec(r'/api/timeline', TimelineHandler),
            tornado.web.URLSpec(r'/api/map', MapHandler),
            tornado.web.URLSpec(r'/login', LoginHandler),
            tornado.web.URLSpec(r'/logout', LogoutHandler),
        ]

        current_dir = os.path.dirname(__file__)

        settings = dict(
            template_path=os.path.join(current_dir, 'templates'),
            static_path=os.path.join(current_dir, 'static'),
            login_url='/login',
            debug=options.debug,
            autoescape='xhtml_escape',
            cookie_secret='074cff43374c4c9d4e4136f884baccbe',
            facebook_api_key='417364814995960',
            facebook_secret='271a6b543e1ad1c410dc4e6bf8ccd430',
            google_api_key='AIzaSyCJbY1fY627epIevgIrg_XLViV5VpSOHOw',
        )

        super(Application, self).__init__(handlers, **settings)

        logging.info('Server started on port {0}'.format(options.port))

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
