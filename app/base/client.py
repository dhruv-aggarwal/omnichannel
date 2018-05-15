import csv
import time
from ..settings import BACKEND, AZURE
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
from ..utils.stopwords import STOPWORDS
from ..utils.tokenization import (
    unigrams_and_bigrams, process_tokens, sort_dict_by_value, filter_words
)
import re


class BaseClient(object):
    def __init__(self):
        self.backend = BACKEND
        self.sid = SentimentIntensityAnalyzer()
        self.azure = AZURE
        self.stopwords = STOPWORDS

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

    def create_word_cloud(self, text_list, min_frequency=10, max_words=100):
        word_counts = self.preprocess_text(text_list)
        sorted_word_counts = sort_dict_by_value(word_counts)
        return filter_words(sorted_word_counts, min_frequency, max_words)

    def preprocess_text(self, text_list):
        """Splits a long text into words, eliminates the stopwords.

        Parameters
        ----------
        text : string
            The text to be processed.

        Returns
        -------
        words : dict (string, int)
            Word tokens with associated frequency.
        """
        text = '\n'.join(text_list)

        stopwords = set([i.lower() for i in self.stopwords])

        flags = (re.UNICODE if type(text) is unicode else 0)
        regexp = r"\w[\w']+"

        words = re.findall(regexp, text, flags)
        # remove stopwords
        words = [word for word in words if word.lower() not in stopwords]
        # remove 's
        words = [word[:-2] if word.lower().endswith("'s") else word
                 for word in words]
        # remove numbers
        words = [word for word in words if not word.isdigit()]
        word_counts = unigrams_and_bigrams(words)

        return word_counts

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
