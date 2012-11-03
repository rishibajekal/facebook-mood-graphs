import facebook
import pygeoip
from tornado.web import asynchronous
from handlers.base import BaseHandler
import simplejson as json


class FBStatusHandler(BaseHandler):

    @asynchronous
    def get(self):
        # Get statuses for user
        user = json.loads(self.get_current_user())
        graph = facebook.GraphAPI(user["access_token"])
        status_request = """[{"method":"GET","relative_url":"method/fql.query?query=select+message,time+from+status+where+uid=me()"}]"""
        feed = graph.request("", post_args={"batch": status_request})
        for status in json.loads(feed[0]["body"]):
            print status
        # TODO:
        # if person exists in mongo:
        #   pass
        # else:
        #   do following and add info to mongo

        # Get location for user
        ip_addr = self.request.remote_ip
        if ip_addr is not None:
            ip_addr = '192.17.253.25'  # we will remove this before pushing it to production
            gi = pygeoip.GeoIP('GeoLiteCity.dat', pygeoip.MEMORY_CACHE)
            address = gi.record_by_addr(ip_addr)
            lat = address['latitude']
            lng = address['longitude']
            # change the format of the lng lat to suharsh format and then push it to mongo
            print lat, lng
        self.finish()
