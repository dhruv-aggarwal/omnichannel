from settings import TWITTER
from tweepy import API, OAuthHandler, TweepError


class TwitterClient:
    def __init__(self):
        self.page_size = 100

        # keys and tokens from the Twitter Dev Console
        self.consumer_key = TWITTER['consumer_key']
        self.consumer_secret = TWITTER['consumer_secret']
        self.access_token = TWITTER['access_token']
        self.access_token_secret = TWITTER['access_token_secret']

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = tweepy.OAuthHandler(
                self.consumer_key,
                self.consumer_secret
            )
            # set access token and secret
            self.auth.set_access_token(
                self.access_token,
                self.access_token_secret
            )
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            raise('Error: Authentication Failed')


    def fetch_tweets(self, query, count=self.page_size):
        '''
        Call Twitter API to fetch tweets
        '''
        fetched_tweets = []
        try:
            fetched_tweets = self.api.search(
                q=query,
                count=count,
            )
        except TweepError as e:
            print("Error : {error}".format(error=e))

        return fetched_tweets

