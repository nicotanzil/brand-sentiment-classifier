from twitter.model.twitter_user import TwitterUser

class Tweet:
    def __init__(self, tweet):
        self.text = tweet.text
        self.user = TwitterUser(tweet.user)
        self.created_at = tweet.created_at

    def get_dict_data(self):
        data = {
            "text": self.text,
            "user": self.user,
            "year": self.created_at
        }
        return data