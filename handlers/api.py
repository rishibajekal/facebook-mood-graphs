import facebook
import datetime
from tornado.web import asynchronous
from handlers.base import BaseHandler
import handlers.sentiment as sentiment
import simplejson as json


class TimelineHandler(BaseHandler):

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
        for status in statuses_json:
            new_status = {}

            new_status['status'] = status['message']
            status_date = datetime.datetime.fromtimestamp(int(status['time']))
            new_status['month'] = status_date.strftime("%B")
            status_date = status_date.isocalendar()
            new_status['year'] = status_date[0]
            new_status['week'] = status_date[1]
            new_status['day'] = status_date[2]
            new_status['sentiment'] = status['sentiment']

            min_statuses.append(new_status)

        self.write(json.dumps(min_statuses))
        self.finish()


class MapHandler(BaseHandler):

    @asynchronous
    def get(self):
        db_map = self.application.db['map']
        results = db_map.find({})
        features = []
        for entry in results:
            push_entry = {}
            push_entry["type"] = "Feature"
            push_entry["geometry"] = {"type": "Point", "coordinates": [entry['lng'], entry['lat']]}
            push_entry["properties"] = {"sentiment": entry['avg_sentiment']}
            features.append(push_entry)
        retval = {"type": "FeatureCollection", "features": features}
        self.write(json.dumps(retval))
        self.finish()
