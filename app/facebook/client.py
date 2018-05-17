import logging
import facebook
from settings import FACEBOOK
from ..base import BaseClient


class FacebookClient(BaseClient):
    def __init__(self):
        super(FacebookClient, self).__init__()

        # access_token from the Facebook developers' console
        self.access_token = FACEBOOK['access_token']

        self.page_size = 100

        self.us = FACEBOOK['admin_ids']

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

    def fetch_feeds(self, query, count):
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

    def parse_feeds(self, feeds):
        parsed_feeds = []

        try:
            for feed in feeds:
                if tweet.author.id in self.us:
                    continue

                parsed_tweet = {
                    'twitter_id': tweet.id,
                    'text': tweet.text,
                    'created_at': tweet.created_at,
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

                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in parsed_feeds:
                        parsed_feeds.append(parsed_tweet)
                else:
                    parsed_feeds.append(parsed_tweet)
        except Exception as e:
            logging.exception(e)

        return parsed_feeds


def connect(access_token, user):
    graph = fb.GraphAPI(access_token)
    profile = graph.get_object(user)

    return graph, profile


def main():

    access_token = FLAGS.access_token
    user = FLAGS.profile

    graph, profile = connect(access_token, user)

    posts = graph.get_connections(profile['id'], 'posts')


    #Let's grab all the posts and analyze them!
    while True:
        try:
            [sentiment_analysis(post=post) for post in posts['data']]
            posts= requests.get(posts['paging']['next']).json()
        except KeyError:
            break



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Simple Facebook Sentiment Analysis Script')
    parser.add_argument('--access_token', type=str, required=True, default='', help='Your Facebook API Access Token: https://developers.facebook.com/docs/graph-api/overview')
    parser.add_argument('--profile', type=str, required=True, default='', help='The profile name to retrieve the posts from')
    FLAGS = parser.parse_args()
    main()
