import requests
from settings import ANDROID_APPS
from ..base_client import BaseClient


class PlayStoreClient(BaseClient):
    def __init__(self):
        super(Freshdesk, self).__init__()
        self.base_url = 'https://www.googleapis.com/androidpublisher'
        self.api_version = 'v3'
        self.package_name = 'my_package_name'
        self.fetch_url = 'applications/{0}/reviews'.format(self.package_name)
        self.page_limit = 10
        self.apps = ANDROID_APPS

    def fetch_reviews(self, app_id, country, data_format, sorting_order):
        page = 0
        responses = []
        while page < self.page_limit:
            page += 1
            response = requests.get(
                "{0}/{1}/{2}".format(
                    self.base_url,
                    self.api_version,
                    self.fetch_url
                )
            )
            # print response.json()
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
