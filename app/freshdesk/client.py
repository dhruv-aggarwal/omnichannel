import requests
from settings import CRM
from ..base import BaseClient


class FreshdeskClient(BaseClient):
    def __init__(self):
        super(Freshdesk, self).__init__()
        self.domain = CRM['freshdesk']['domain']
        self.api_key = CRM['freshdesk']['api_key']
        self.password = CRM['freshdesk']['password']
        self.api_version = 'v2'
        self.base_url = \
            'https://{domain}.freshdesk.com/api/{api_version}/'.format(
                domain=self.domain,
                api_version=self.api_version
            )
        self.fetch_url = 'tickets'
        self.page_size = 100
        self.page_limit = 100
        self.source_map = {
            '1': 'Email',
            '2': 'Portal',
            '3': 'Phone',
            '7': 'Chat',
            '8': 'Mobihelp',
            '9': 'Feedback Widget',
            '10': 'Outbound Email'
        }
        self.status_map = {
            '2': 'open',
            '3': 'pending',
            '4': 'resolved',
            '5': 'closed'
        }
        self.priority_map = {
            '1': 'low',
            '2': 'medium',
            '3': 'high',
            '4': 'urgent'
        }

    def fetch_tickets(self):
        page = 0
        responses = []
        while 1:
            page += 1
            response = requests.get(
                self.base_url + self.fetch_url,
                params={
                    'order_by': 'created_at',
                    'order_type': 'desc',
                    'per_page': self.page_size,
                    'page': page
                },
                auth=(self.api_key, self.password)
            )
            if not response.json():
                break
            responses += response.json()
        return self.parse_response(responses)

    def parse_response(self, responses):
        parsed = []
        for item in responses:
            parsed.append({
                'subject': item['subject'],
                'created_at': item['created_at'],
                'description_text': item['description_text'],
                'product_id': item['product_id'],
                'email': item.get('email'),
                'sentiment': item['custom_fields'].get('sentiment'),
                'csat_rating': item['custom_fields'].get('csat_rating'),
                'country': item['custom_fields'].get('country'),
                'platform': item['custom_fields'].get('platform'),
                'practo_source': item['custom_fields'].get('practo_source'),
                'practo_product': item['custom_fields'].get('practo_product'),
                'source': self.source_map.get(item['source']),
                'priority': self.priority_map.get(item['priority']),
                'type': item['type']
            })
        return parsed
