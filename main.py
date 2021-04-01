from flask import Flask
from flask_restful import Api, Resource

from twitter.stream_tweets import Twitter

app = Flask(__name__)
api = Api(app)

twitter = Twitter()

keywords = {}

# class HelloWorld(Resource):
#     def get(self, name):
#         return names[name]
#
#     def post(self):
#         return {"data": "Post"}

class Query(Resource):
    def get(self, keyword):
        tweets = twitter.fetch_tweet_by_query(query=keyword)
        #print(twitter.fetch_tweet_by_query(query=keyword))
        return {"tweets": tweets}


api.add_resource(Query, "/query/<string:keyword>")

if __name__ == "__main__":
    app.run(debug=True)
