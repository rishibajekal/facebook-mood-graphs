from tornado.web import authenticated
from handlers.base import BaseHandler


class IndexHandler(BaseHandler):
    """Handler to render index page"""

    def get(self):
        self.render('index.html')


class DisplayHandler(BaseHandler):
    """Handler to render display page"""

    @authenticated
    def get(self):
        self.render('display.html')
