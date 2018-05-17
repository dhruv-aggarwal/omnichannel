import collections
import csv
from itertools import izip_longest
import json
import logging
import requests
import re
import time
import nltk
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')
from nltk import tokenize
from nltk.corpus import stopwords as nltk_stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import wordpunct_tokenize
from settings import BACKEND, AZURE, AWS
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import boto3
from ..utils.stopwords import STOPWORDS
from ..utils.tokenization import (
    unigrams_and_bigrams, process_tokens, sort_dict_by_value, filter_words
)
from nltk.stem import WordNetLemmatizer


class BaseClient(object):
    def __init__(self):
        self.backend = BACKEND
        self.sid = SentimentIntensityAnalyzer()
        self.azure = AZURE
        self.stopwords = STOPWORDS
        self.wordnet_lemmatizer = WordNetLemmatizer()

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
        text = ' '.join(text_list)

        stopwords = set([i.lower() for i in self.stopwords])
        stopwords = stopwords.union(nltk_stopwords.words())

        # remove 's
        words = [
            i.lower()[:-2] if i.lower().endswith("'s") else i.lower()
            for i in wordpunct_tokenize(text)
            if i.lower() not in stopwords and i.isalpha()
        ]
        words = self.lemmatize(words)
        word_counts = unigrams_and_bigrams(words)

        return word_counts

    def get_sentiment_score_from_nltk(self, text_list):
        sentiments = {}

        for item in text_list:
            sentiments[item] = self.sid.polarity_scores(item)

        return sentiments

    def get_sentiment_score_from_azure(self, text_list):
        sentiments = {}
        text_indexes = {}

        documents = {'documents': []}
        for index, item in enumerate(text_list):
            documents['documents'].append({
                'id': index,
                'language': 'en',
                'text': item
            })
            text_indexes[str(index)] = item
        headers = {
            "Ocp-Apim-Subscription-Key": self.azure['keys'][0]
        }
        response = requests.post(
            '{base_url}/{version}/{sentiment_url_suffix}'.format(
                base_url=self.azure['url'],
                version=self.azure['api_version'],
                sentiment_url_suffix=self.azure['sentiment_url_suffix']
            ),
            headers=headers,
            json=documents
        )
        response = response.json()
        for item in response['documents']:
            sentiments[text_indexes[item['id']]] = item['score']

        return sentiments

    def get_sentiment_score_from_gcloud(self, text_list):
        sentiments = {}

        client = language.LanguageServiceClient()
        for index, text in enumerate(text_list):
            document = types.Document(
                content=text,
                type=enums.Document.Type.PLAIN_TEXT
            )
            annotations = client.analyze_sentiment(document=document)
            sentiments[text] = {
                'score': annotations.document_sentiment.score,
                'magnitude': annotations.document_sentiment.magnitude
            }

        return sentiments

    def get_sentiment_score_from_amazon_comprehend(self, text_list):
        sentiments = {}

        comprehend = boto3.client(
            'comprehend',
            aws_access_key_id=AWS['access_key_id'],
            aws_secret_access_key=AWS['secret_access_key'],
            region_name=AWS['region']
        )
        batched_text_list = [
            text_list[i:i + AWS['batch_size']]
            for i in range(0, len(text_list), AWS['batch_size'])
        ]
        for index, batch_text_list in enumerate(batched_text_list):
            try:
                batch_response = comprehend.batch_detect_sentiment(
                    TextList=batch_text_list,
                    LanguageCode='en'
                )
            except Exception as e:
                logging.exception(e)
            for response in batch_response['ResultList']:
                sentiments[batch_text_list[response['Index']]] = {
                    'sentiment': response['Sentiment'],
                    'score': response['SentimentScore'],
                }

        return sentiments

    def get_sentiment_scores(self, algorithm, text_list):
        if algorithm == 'nltk':
            return self.get_sentiment_score_from_nltk(text_list)
        elif algorithm == 'azure':
            return self.get_sentiment_score_from_azure(text_list)
        elif algorithm == 'gcloud':
            return self.get_sentiment_score_from_gcloud(text_list)
        elif algorithm == 'az_comprehend':
            return self.get_sentiment_score_from_amazon_comprehend(text_list)
        else:
            raise Exception('Invalid algorithm')

    def lemmatize(self, words):
        lemmatized_words = set()
        for word in words:
            if hasattr(word, "__iter__"):
                lemmatized_words.add(
                    self.wordnet_lemmatizer.lemmatize(word[0], word[1])
                )
            else:
                lemmatized_words.add(self.wordnet_lemmatizer.lemmatize(word))
        return list(lemmatized_words)
