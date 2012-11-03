from tornado.auth import FacebookGraphMixin
from tornado.web import asynchronous
from handlers.base import BaseHandler


class FacebookLogin(BaseHandler, FacebookGraphMixin):

    @asynchronous
    def get(self):
        if self.get_argument("code", False):
            self.get_authenticated_user(
                redirect_uri='http://localhost:8888/login',
                client_id=self.application.settings["facebook_api_key"],
                client_secret=self.application.settings["facebook_secret"],
                code=self.get_argument("code"),
                callback=self.async_callback(self._on_login)
            )
            return
        self.authorize_redirect(redirect_uri='http://localhost:8888/login',
                                client_id=self.settings["facebook_api_key"],
                                extra_params={"scope": "read_stream,offline_access"})

    def _on_login(self, user):
        print user
        self.finish()
