import facebook
import tornado.web
from tornado.auth import FacebookGraphMixin
from tornado.web import asynchronous
from handlers.base import BaseHandler
import handlers.sentiment as sentiment


class LogoutHandler(BaseHandler):
    @asynchronous
    def get(self):
        self.clear_cookie("user")
        self.redirect('/')


class LoginHandler(BaseHandler, FacebookGraphMixin):

    @asynchronous
    def get(self):
        if self.get_argument("code", False):
            self.get_authenticated_user(
                redirect_uri='http://sentipede.herokuapp.com/login',
                client_id=self.application.settings["facebook_api_key"],
                client_secret=self.application.settings["facebook_secret"],
                code=self.get_argument("code"),
                callback=self.async_callback(self._on_login)
            )
            return
        self.authorize_redirect(redirect_uri='http://sentipede.herokuapp.com/login',
                                client_id=self.settings["facebook_api_key"],
                                extra_params={"scope": "read_stream,offline_access"})

    def _on_login(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Facebook authentication failed. Please try again.")
        self.set_secure_cookie("user", tornado.escape.json_encode(user))
        self.add_user(user)
        self.redirect('/timeline')

    def add_user(self, user):
        db_map = self.application.db['map']

        results = db_map.find_one({'_id': user['id']})

        if results is None:
            # Get statuses from user from Facebook
            graph = facebook.GraphAPI(user["access_token"])
            status_request = """[{"method":"GET","relative_url":"method/fql.query?query=select+message,time+from+status+where+uid=me()"}]"""
            statuses = graph.request("", post_args={"batch": status_request})

            # Generate sentiments
            statuses_json = sentiment.sentimentJSON((statuses[0]["body"]), self.application.classifier)

            # Calculate average sentiment for user
            avg_sentiment = 0
            num_statuses = 0
            for status in statuses_json:
                avg_sentiment += status['sentiment']
                num_statuses += 1
            # Calculate average sentiment
            avg_sentiment /= num_statuses

            # Get location for user
            user_id = user['id']
            geo_lng = float(self.get_cookie("geo_lng"))
            geo_lat = float(self.get_cookie("geo_lat"))
            if geo_lng is not None and geo_lat is not None:
                db_map.insert({'_id': user_id, 'avg_sentiment': avg_sentiment, 'lat': geo_lat, 'lng': geo_lng})
            else:
                db_map.insert({'_id': user_id, 'avg_sentiment': avg_sentiment})
