import facebook
from googlemaps import GoogleMaps
from tornado.web import asynchronous
from handlers.base import BaseHandler
import simplejson as json


class FBStatusHandler(BaseHandler):

    @asynchronous
    def get(self):
        user = json.loads(self.get_current_user())
        graph = facebook.GraphAPI(user["access_token"])
        status_request = """[{"method":"GET","relative_url":"method/fql.query?query=select+message,time,place_id+from+status+where+uid=me()"}]"""
        feed = graph.request("", post_args={"batch": status_request})
        for status in json.loads(feed[0]["body"]):
            print status
        person = graph.get_object("me")
        person = json.loads(json.dumps(person))
        location = person["location"]
        location_name = location['name']
        gmaps = GoogleMaps('AIzaSyCJbY1fY627epIevgIrg_XLViV5VpSOHOw')
        lat, lng = gmaps.address_to_latlng(location_name)
