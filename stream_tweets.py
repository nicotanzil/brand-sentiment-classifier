from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from tweepy import API
from tweepy import Cursor

import twitter_credentials

import numpy as np
import pandas as pd

import re


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

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
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


class TweetAnalyzer:
    """
    Functionality for analyzing and categorizing contents from tweets
    """

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=tweets)

        df['id'] = np.array([tweet.id for tweet in tweets])
        df['text'] = np.array([tweet.text for tweet in tweets])
        df['screen_name'] = np.array([tweet.author.screen_name for tweet in tweets])
        df['created_at'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['favorite'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweet'] = np.array([tweet.retweet_count for tweet in tweets])

        return df


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
        fetched_tweets = self.api.user_timeline(screen_name=screen_name, count=count)
        return fetched_tweets

    def fetch_tweet_by_query(self, query=None, count=5):
        fetched_tweets = self.api.search(q=query, lang="en", count=count)
        return fetched_tweets

    def fetch_tweet_by_hashtags(self, hashtags=[], count=5):
        pass


class TweetPreprocessing:

    def __init__(self):
        pass

    def clean(self, tweet_to_clean):
        tweet_to_clean = re.sub(r'^RT[\s]+', '', tweet_to_clean)
        tweet_to_clean = re.sub(r'https?://.*[\r\n]*', '', tweet_to_clean)
        tweet_to_clean = re.sub(r'#', '', tweet_to_clean)
        tweet_to_clean = re.sub(r'@[A-Za-z0–9]+', '', tweet_to_clean)
        return tweet_to_clean


if __name__ == "__main__":
    # Get all the necessary class
    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()
    tweet_preprocessing = TweetPreprocessing()

    # Get the API
    twitter_api = twitter_client.get_twitter_client_api()
    tweet_fetcher = TweetDataFetcher(api=twitter_api)

    # Variable
    screen_name = "iphone"
    hash_tag_list = ["GalaxyA52", "SamsungGalaxy", "GalaxyA", "GalaxyA72", "GalaxyS21"]

    query = "iphone"
    tweets_per_query = 10
    file_name = 'query.txt'
    since_id = None

    # Fetch all necessary data
    tweets_by_user = tweet_fetcher.fetch_tweet_by_screen_name(screen_name=screen_name, count=10)
    tweets_by_query = tweet_fetcher.fetch_tweet_by_query(query=query, count=tweets_per_query)

    # Convert tweets to data frame
    # df = tweet_analyzer.tweets_to_data_frame(tweets_by_user)
    df = tweet_analyzer.tweets_to_data_frame(tweets_by_query)

    cleaned_tweets = []

    for tweet in df['text']:
        cleaned_tweets.append(tweet_preprocessing.clean(tweet))
        # print("Before: \t", tweet)
        print("After: \t", tweet_preprocessing.clean(tweet), end="\n\n")

    for tweet in cleaned_tweets:
        print(tweet)

    # print(df)
    # print(len(df))
    # print(df['text'])
    # print(df['screen_name'])
    # print(df['favorite'])
    # print(df['retweet'])

    #
    # twitter_streamer = TwitterStreamer()
    # twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)

    # twitter_client = TwitterClient('verified')
    # # print(twitter_client.get_user_timeline_tweets(1))
    # print(twitter_client.get_friend_list(3))
