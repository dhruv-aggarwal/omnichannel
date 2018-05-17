from .client import FacebookClient


def fetch_data(query, count=None):
    '''
    Main function to fetch feeds and parse them.
    '''
    parsed = []
    # creating object of FacebookClient Class
    client = FacebookClient()
    # calling functions to get feeds and parse
    feeds = client.fetch_feeds(query, count)
    parsed = client.parse_feeds(feeds)

    return parsed
