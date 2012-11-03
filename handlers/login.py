import facebook
import tornado.web
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
        if not user:
            raise tornado.web.HTTPError(500, "Facebook authentication failed. Please try again.")
        self.set_secure_cookie("user", tornado.escape.json_encode(user))
        graph = facebook.GraphAPI(user["access_token"])
        batched_requests = '[{"method":"GET","relative_url":"me"}, {"method":"GET","relative_url":"me/feed?limit=50"}]'
        feed = graph.request("", post_args={"batch": batched_requests})
        print feed
        self.redirect('/display')
