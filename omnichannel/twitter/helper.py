# from textblob import TextBlob
import re
from .client import TwitterClient
from settings import TWITTER


# def get_tweet_sentiment(tweet):
#     '''
#     Utility function to classify sentiment of passed tweet
#     using textblob's sentiment method
#     '''
#     # create TextBlob object of passed tweet text
#     analysis = TextBlob(tweet)
#     # set sentiment
#     if analysis.sentiment.polarity > 0:
#         return 'positive'
#     elif analysis.sentiment.polarity == 0:
#         return 'neutral'
#     else:
#         return 'negative'


# def sentiment_analysis(tweets):
#     # picking positive tweets from tweets
#     ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
#     # percentage of positive tweets
#     print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
#     # picking negative tweets from tweets
#     ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
#     # percentage of negative tweets
#     print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
#     # percentage of neutral tweets
#     print("Neutral tweets percentage: {} % \
#         ".format(100*len(tweets - ntweets - ptweets)/len(tweets)))

#     # printing first 5 positive tweets
#     print("\n\nPositive tweets:")
#     for tweet in ptweets[:10]:
#         print(tweet['text'])

#     # printing first 5 negative tweets
#     print("\n\nNegative tweets:")
#     for tweet in ntweets[:10]:
#         print(tweet['text'])


# def clean_tweet(tweet):
#     '''
#     Utility function to clean tweet text by removing links, special characters
#     using simple regex statements.
#     '''
#     return ' '.join(
#         re.sub(
#             "(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)",
#             " ",
#             tweet
#         ).split()
#     )


def parse_tweets(tweets):
    parsed_tweets = []

    for tweet in tweets:
        if tweet.author.id in TWITTER['practo_ids']:
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

        # saving sentiment of tweet
        # parsed_tweet['sentiment'] = get_tweet_sentiment(clean_tweet(tweet.text))

        if tweet.retweet_count > 0:
            # if tweet has retweets, ensure that it is appended only once
            if parsed_tweet not in parsed_tweets:
                parsed_tweets.append(parsed_tweet)
        else:
            parsed_tweets.append(parsed_tweet)

    return parsed_tweets


def get_tweets(query, count=None):
    '''
    Main function to fetch tweets and parse them.
    '''
    # creating object of TwitterClient Class
    client = TwitterClient()
    # calling function to get tweets
    tweets = client.fetch_tweets(query, count)

    parsed_tweets = parse_tweets(tweets)

    return parsed_tweets
