import csv
from settings imoprt REVIEW_DATA_FILE, WORDCLOUD_DATA_FILE


def parse_to_word_cloud():
    wordcloud_data = []

    with open(REVIEW_DATA_FILE, 'rb') as review_file:
        reader = csv.reader(review_file)
        for review in reader:
            wordcloud_data.append({

            })

    with open(WORDCLOUD_DATA_FILE, 'wb') as wordcloud_file:
        dict_writer = csv.DictWriter(wordcloud_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(toCSV)
