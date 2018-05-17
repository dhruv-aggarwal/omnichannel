import logging
import tweepy
from settings import TWITTER
from ..base import BaseClient


class TwitterClient(BaseClient):
    def __init__(self):
        super(TwitterClient, self).__init__()

        # keys and tokens from the Twitter Dev Console
        self.consumer_key = TWITTER['consumer_key']
        self.consumer_secret = TWITTER['consumer_secret']
        self.access_token = TWITTER['access_token']
        self.access_token_secret = TWITTER['access_token_secret']

        self.page_size = 100

        self.us = TWITTER['admin_ids']

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
            raise Exception('Authentication Failed')

    def fetch_tweets(self, query, count):
        '''
        Call Twitter API to fetch tweets
        '''
        count = count or self.page_size
        fetched_tweets = []
        try:
            fetched_tweets = self.api.search(
                q=query,
                count=count,
            )
        except tweepy.TweepError as e:
            logging.exception(e)

        return fetched_tweets

    def push_data_to_backend(self):
        parsed = []
        for query in QUERIES:
            reviews = self.fetch_tweets(query, None)
            parsed += self.parse_tweets(reviews)
        self.save_review_data(reviews)

    def parse_tweets(self, tweets):
        parsed_tweets = []

        try:
            for tweet in tweets:
                if tweet.author.id in self.us:
                    continue

                parsed_tweet = {
                    'source': 'Twitter',
                    'text': tweet.text,
                    'date': tweet.created_at,
                    'metacontent': {
                        'twitter_id': tweet.id,
                        'author': {
                            'twitter_id': tweet.author.id,
                            'name': tweet.author.name,
                            'created_at': tweet.author.created_at,
                            'location': tweet.author.location,
                            'screen_name': tweet.author.screen_name,
                        },
                        'language': tweet.lang,
                        'favorite_count': tweet.favorite_count,
                        'retweet_count': tweet.retweet_count,
                        'reply_to_author_id': tweet.in_reply_to_user_id,
                        'reply_to_twitter_id': tweet.in_reply_to_status_id,
                    }
                }

                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in parsed_tweets:
                        parsed_tweets.append(parsed_tweet)
                else:
                    parsed_tweets.append(parsed_tweet)
        except Exception as e:
            logging.exception(e)

        return parsed_tweets
