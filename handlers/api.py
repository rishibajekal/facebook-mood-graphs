import facebook
from tornado.web import asynchronous
from handlers.base import BaseHandler
import simplejson as json


class FBStatusHandler(BaseHandler):

    @asynchronous
    def get(self):
        user = json.loads(self.get_current_user())
        graph = facebook.GraphAPI(user["access_token"])
        status_request = """[{"method":"GET","relative_url":"method/fql.query?query=select+message,time+from+status+where+uid=me()"}]"""
        feed = graph.request("", post_args={"batch": status_request})
        for status in json.loads(feed[0]["body"]):
            print status
