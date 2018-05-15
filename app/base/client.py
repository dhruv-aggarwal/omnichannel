import csv
import time
from settings import BACKEND, AZURE
from wordcloud import WordCloud
import nltk
nltk.download('vader_lexicon')
nltk.download('punkt')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
import requests
import collections
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


class BaseClient(object):
    def __init__(self):
        self.backend = BACKEND
        self.wc = WordCloud()
        self.sid = SentimentIntensityAnalyzer()
        self.azure = AZURE

    def save_data(self, list_of_dict):
        if self.backend == 'csv':
            file_name = "{source}|{timestamp}".format(
                source=self.__class__.__name__,
                timestamp=time.time()
            )
            self.write_as_csv(file_name, list_of_dict)
        else:
            print 'Unknown source'

    def write_as_csv(self, file_name, list_of_dict):
        keys = list_of_dict[0].keys()
        with open(file_name, 'wb') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(toCSV)

    def get_word_frequencies(self, text_list):
        return self.wc.process_text('\n'.join(text_list))

    def get_sentiment_score_from_nltk(self, text_list):
        sentiments = []
        for item in text_list:
            ss = sid.polarity_scores(item)
            sentiments.append(ss)
        return sentiments

    def get_sentiment_score_from_azure(self, text_list):
        od = collections.OrderedDict()
        documents = {'documents': []}
        for index, item in enumerate(text_list):
            documents['documents'].append({
                'id': index,
                'language': 'en',
                'text': item
            })
        headers = {
            "Ocp-Apim-Subscription-Key": self.azure.keys[0]
        }
        response = requests.post(
            '{base_url}/{version}/{sentiment_url_suffix}'.format(
                self.azure['url'],
                self.azure['api_version'],
                self.azure['sentiment_url_suffix']
            ),
            headers=headers,
            json=documents
        )
        response = response.json()
        for item in response['documents']:
            od[item['id']] = item['score']
        return od.values()

    def get_sentiment_score_from_gcloud(self, text_list):
        sentiments = []
        client = language.LanguageServiceClient()
        for index, text in enumerate(text_list):
            document = types.Document(
                content=text,
                type=enums.Document.Type.PLAIN_TEXT
            )
            annotations = client.analyze_sentiment(document=document)
            sentiments.append({
                'score': annotations.document_sentiment.score,
                'magnitude': annotations.document_sentiment.magnitude
            })

        return sentiments

    def get_sentiment_scores(self, algorithm, text_list):
        if algorithm == 'nltk':
            return self.get_sentiment_score_from_nltk(text_list)
        elif algorithm == 'azure':
            return self.get_sentiment_score_from_azure(text_list)
        elif algorithm == 'gcloud':
            return self.get_sentiment_score_from_gcloud(text_list)
        else:
            raise Exception('Invalid algorithm')
