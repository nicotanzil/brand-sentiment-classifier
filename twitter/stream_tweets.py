from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from tweepy import API
from tweepy import Cursor

import numpy as np
import pandas as pd

from twitter import twitter_credentials as tc
from twitter.model import tweet as t

import preprocessor as p

from services.encoder import DateTimeEncoder
from twitter.sentiment_analysis import SentimentAnalysis

from datetime import date, datetime, timedelta

import random

# TWITTER CLIENT
class TwitterClient:
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(home_timeline_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets


# TWITTER AUTHENTICATOR
class TwitterAuthenticator:

    """
    Authenticating the Twitter API access with key
    """

    def authenticate_twitter_app(self):
        auth = OAuthHandler(tc.CONSUMER_KEY, tc.CONSUMER_SECRET)
        auth.set_access_token(tc.ACCESS_TOKEN, tc.ACCESS_TOKEN_SECRET)
        return auth


# TWITTER STREAMER
class TwitterStreamer:
    """
    Class for streaming and processing live tweets.
    """

    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authentication and the connection to the Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()

        stream = Stream(auth, listener)

        stream.filter(track=hash_tag_list)


class TwitterListener(StreamListener):
    """
    This is a basic listener class that just prints received tweets to stdout
    """

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print('Error on data: %s' % str(e))
        return True

    def on_error(self, status_code):
        if status_code == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status_code)


class TweetDataFetcher:
    """
    Functionality for fetching tweets data for various category, such as:
        - User (screen_name)
        - Keyword
        - Hashtags
    """

    def __init__(self, api):
        self.api = api
        pass

    def fetch_tweet_by_screen_name(self, screen_name=None, count=5):
        fetched_tweets = self.api.user_timeline(screen_name=screen_name, count=count, include_rts=False, tweet_mode='extended')
        return fetched_tweets

    def fetch_tweet_by_query(self, query=None, count=5, result_type="mixed"):
        fetched_tweets = self.api.search(q=query, lang="en", count=count, result_type=result_type)
        return fetched_tweets

    def fetch_tweet_by_hashtags(self, hashtags=[], count=5):
        pass

    def fetch_tweet_by_query_last_week(self, query=None, count=5):
        tweets_list = []
        classifier = SentimentAnalysis()
        for i in range(7):
            pos_count, neg_count = 0, 0
            fromDate = datetime.now() - timedelta(days=7-i+1)
            toDate = datetime.now() - timedelta(days=7-i)
            print(f"From: {fromDate} To: {toDate}")
            fromDate = fromDate.strftime("%Y%m%d%H%M")
            toDate = toDate.strftime("%Y%m%d%H%M")
            # yyyyMMddHHmm
            """
            #LIMITED AMOUNT OF REQUEST AT 250 REQ/MONTH! USE WITH CAUTION
            fetched_tweets = self.api.search_30_day(environment_name='dev', query=query, fromDate=fromDate, toDate=toDate, maxResults=count)
            for tweet in fetched_tweets:
                if classifier.classify_tweets(tweet) == "Positive":
                    pos_count += 1
                else:
                    neg_count += 1
            """
            pos_count = random.randint(1, 75)
            neg_count = 100 - pos_count
            temp = {
                "date": str(datetime.now() - timedelta(days=7-i+1)),
                "pos_count": pos_count,
                "neg_count": neg_count
            }
            tweets_list.append(temp)

        return tweets_list

class Twitter:
    def __init__(self):
        self.twitter_client = TwitterClient()

        # Get the API
        self.twitter_api = self.twitter_client.get_twitter_client_api()
        self.tweet_fetcher = TweetDataFetcher(api=self.twitter_api)

    def fetch_tweet_by_query(self, query=None, count=5, result_type="mixed"):
        classifier = SentimentAnalysis()
        
        fetched_tweets = self.tweet_fetcher.fetch_tweet_by_query(query, count=count, result_type=result_type)

        tweets_list = []
        for tweet in fetched_tweets:
            try:
                _ = tweet.entities["media"]
            except:
                print("NO MEDIA :(")
            temp = {
                "id": tweet.id_str,
                "text": tweet.text,
                "user": {
                    "id": tweet.user.id,
                    "name": tweet.user.name,
                    "screen_name": tweet.user.screen_name,
                    "profile_image_url": tweet.user.profile_image_url,
                    "created_at": str(tweet.user.created_at),
                },
                "created_at": str(tweet.created_at),
                "entities": {
                    "hashtags": tweet.entities["hashtags"],
                    "media": None,
                },
                "retweet_count": tweet.retweet_count,
                "favorite_count": tweet.favorite_count,
                "sentiment": classifier.classify_tweets(tweet.text)
            }
            try:
                temp["entities"]["media"] = tweet.entities["media"]
            except:
                print("no media")
            print("---------------------")

            tweets_list.append(temp)

        return tweets_list

    def fetch_last_week_tweets(self, query=None, count=100):
        last_week_tweet = self.tweet_fetcher.fetch_tweet_by_query_last_week(query=query, count=count)
        print("LAST WEEK TWEETS")
        print(last_week_tweet)
        return last_week_tweet
    
    def fetch_tweet_by_user(self, screen_name, count=10):
        classifier = SentimentAnalysis()

        fetched_tweets = self.tweet_fetcher.fetch_tweet_by_screen_name(screen_name=screen_name, count=count)

        tweets_list = []
        for tweet in fetched_tweets:
            try:
                _ = tweet.entities["media"]
            except:
                print("NO MEDIA :(")
            temp = {
                "id": tweet.id_str,
                "text": tweet.full_text,
                "user": {
                    "id": tweet.user.id,
                    "name": tweet.user.name,
                    "screen_name": tweet.user.screen_name,
                    "profile_image_url": tweet.user.profile_image_url,
                    "created_at": str(tweet.user.created_at),
                },
                "created_at": str(tweet.created_at),
                "entities": {
                    "hashtags": tweet.entities["hashtags"],
                    "media": None,
                },
                "retweet_count": tweet.retweet_count,
                "favorite_count": tweet.favorite_count,
                "sentiment": classifier.classify_tweets(tweet.full_text)
            }
            try:
                temp["entities"]["media"] = tweet.entities["media"]
            except:
                print("no media")
            print("---------------------")

            tweets_list.append(temp)
        return tweets_list
        