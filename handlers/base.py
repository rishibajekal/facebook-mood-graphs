from tornado.web import RequestHandler


class BaseHandler(RequestHandler):
    """BaseHandler for RequestHandlers to inherit from"""

    def get_current_user(self):
        user = self.get_secure_cookie("user")
        return user
