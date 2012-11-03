from tornado.web import authenticated
from handlers.base import BaseHandler


class IndexHandler(BaseHandler):
    """Handler to render index page"""

    def get(self):
        self.render('index.html')


class TimelineHandler(BaseHandler):
    """Handler to render timeline page"""

    @authenticated
    def get(self):
        self.render('timeline.html')


class LocationHandler(BaseHandler):
    """Handler to render index page"""

    def get(self):
        self.render('location.html')


class LikesHandler(BaseHandler):
    """Handler to render index page"""

    def get(self):
        self.render('likes.html')
