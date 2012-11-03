from tornado.web import authenticated
from handlers.base import BaseHandler


class IndexPageHandler(BaseHandler):
    """Handler to render index page"""

    def get(self):
        self.render('index.html')


class TimelinePageHandler(BaseHandler):
    """Handler to render timeline page"""

    @authenticated
    def get(self):
        self.render('timeline.html')


class LocationPageHandler(BaseHandler):
    """Handler to render index page"""

    def get(self):
        self.render('location.html')


class LikesPageHandler(BaseHandler):
    """Handler to render index page"""

    def get(self):
        self.render('likes.html')
