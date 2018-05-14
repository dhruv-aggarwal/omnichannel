import requests
from settings import IOS_APPS
from ..base import BaseClient


class AppStoreClient(BaseClient):
    def __init__(self):
        super(Freshdesk, self).__init__()
        self.base_url = 'https://itunes.apple.com/'
        self.fetch_url = '{country}/rss/customerreviews/page={page}/id={app_id}/sortby={sorting_order}/{data_format}'
        self.page_limit = 10
        self.apps = IOS_APPS

    def fetch_reviews(self, app_id, country, data_format, sorting_order):
        page = 0
        responses = []
        while page < self.page_limit:
            page += 1
            response = requests.get(
                self.base_url + self.fetch_url.format(
                    page=page,
                    app_id=app_id,
                    sorting_order=sorting_order,
                    data_format=data_format,
                    country=country
                )
            )
            responses.append(response.json())
        return self.parse_response(responses)

    def fetch_provider_app_reviews(
        self, country='in', data_format='json', sorting_order='mostRecent'
    ):
        return self.fetch_reviews(
            self.apps['provider']['id'],
            country,
            data_format,
            sorting_order
        )

    def fetch_consumer_app_reviews(
        self, country='in', data_format='json', sorting_order='mostRecent'
    ):
        return self.fetch_reviews(
            self.apps['consumer']['id'],
            country,
            data_format,
            sorting_order
        )

    def parse_response(self, responses):
        parsed = []
        for item in responses:
            for entry in item['feed'].get('entry', []):
                if 'author' not in entry:
                    continue
                parsed.append({
                    'version': entry['im:version']['label'],
                    'title': entry['title']['label'],
                    'vote_count': entry['im:voteCount']['label'],
                    'rating': entry['im:rating']['label'],
                    'id': entry['id']['label'],
                    'review': entry['content']['label'],
                    'author_url': entry['author']['uri']['label'],
                    'author': entry['author']['name']['label']
                })
        return parsed
