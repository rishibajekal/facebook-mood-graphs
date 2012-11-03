import facebook
from googlemaps import GoogleMaps
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

        # Get location for user
        person = graph.get_object("me")
        if "location" in person:
            # TODO:
            # if person exists in mongo:
            #   pass
            # else:
            #   do following and add info to mongo

            location = person["location"]
            location_name = location['name']
            gmaps = GoogleMaps(self.application.settings.google_api_key)
            lat, lng = gmaps.address_to_latlng(location_name)

        self.finish()
