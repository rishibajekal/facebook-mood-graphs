import facebook
import pygeoip
import datetime
from tornado.web import asynchronous
from handlers.base import BaseHandler
import handlers.sentiment as sentiment
import simplejson as json


class MapHandler(BaseHandler):

    @asynchronous
    def get(self):

        db_map = self.application.db['map']
        results = db_map.find({})
        for entry in results:
            print entry


class CreateHandler(BaseHandler):

    @asynchronous
    def get(self):
        # Get statuses for user from Facebook
        user = json.loads(self.get_current_user())
        graph = facebook.GraphAPI(user["access_token"])
        status_request = """[{"method":"GET","relative_url":"method/fql.query?query=select+message,time+from+status+where+uid=me()"}]"""
        statuses = graph.request("", post_args={"batch": status_request})

        # Generate sentiments
        statuses_json = sentiment.sentimentJSON((statuses[0]["body"]), self.application.classifier)
        min_statuses = []

        # Append week of year and calculate average sentiment for user
        avg_sentiment = 0
        num_statuses = 0
        for status in statuses_json:
            new_status = {}

            status_date = datetime.datetime.fromtimestamp(int(status['time']))
            new_status['month'] = status_date.strftime("%B")
            status_date = status_date.isocalendar()
            new_status['year'] = status_date[0]
            new_status['week'] = status_date[1]
            new_status['day'] = status_date[2]
            new_status['sentiment'] = status['sentiment']

            min_statuses.append(new_status)

            avg_sentiment += status['sentiment']
            num_statuses += 1

        # Calculate average sentiment
        avg_sentiment /= num_statuses
        # user_id # avg_sentiment # lat # lng
        # TODO:
        db_map = self.application.db['map']
        user_id = user['id']
        results = db_map.find_one({'_id': user_id})
        if results is None:
            # Get location for user
            lat = None
            lng = None
            ip_addr = self.request.remote_ip
            if ip_addr is not None:
                ip_addr = '192.17.253.25'  # we will remove this before pushing it to production
                gi = pygeoip.GeoIP('static/resources/GeoLiteCity.dat', pygeoip.MEMORY_CACHE)
                address = gi.record_by_addr(ip_addr)
                lat = address['latitude']
                lng = address['longitude']
            db_map.insert({'_id': user_id, 'avg_sentiment': avg_sentiment, 'lat': lat, 'lng': lng})
        print json.dumps(min_statuses)
        self.write(json.dumps(min_statuses))
        self.finish()
