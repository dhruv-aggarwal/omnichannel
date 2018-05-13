import csv
import time
from settings import BACKEND
from wordcloud import WordCloud


class Base(object):
    def __init__(self):
        self.backend = BACKEND
        self.wc = WordCloud()

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

    def get_word_frequencies(self, text):
        return self.wc.process_text(text)
