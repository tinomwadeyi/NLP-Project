from __future__ import division
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

from fuzzywuzzy import process
from fuzzywuzzy import fuzz

import itertools
import csv
import pprint

topics = []

pairs = []

keywords = []

def keyword_search():

    # Various files used for proof concept
    with open('...', 'rt', encoding='ISO-8859-1') as file_data:
   
        reader = csv.DictReader(file_data, delimiter=",")

        for row in reader:

            # Clean the text recognising terms
            c = Cleaner()

            # Cleans summary
            cleaned = c.clean(row["..."])

            # Removes punctuation
            remove_punctuation = RegexpTokenizer(r'\w+')
            removed = remove_punctuation.tokenize(cleaned)

            # Can be changed to remove specific items from the text
            removal_list = ['_']

            # Removes all occurences from the removal_list
            final_list = [word for word in removed if word not in removal_list]

            # Removes stops from the data
            stop_words = set(stopwords.words('english'))

            # Filters the data of stop words
            filtered_sentence = [w for w in final_list if not w in stop_words]

            # Filter sentences and append to a dictionary
            filtered_sentence = []

            for word in final_list:
                if word not in stop_words:
                    filtered_sentence.append(word)

            topics = row["..."]

            result = ' '.join(filtered_sentence).replace(' , ', ',').replace(' .', '.').replace(' !', '!')
            result = result.replace(' ?', '?').replace(' : ', ': ').replace(' \'', '\'')

            data = {topics : result}

            pairs = {topics : cleaned}
            pairs.append(pairs)

            topics.append(data)

            output = {}

            for d in topics:
                output.update(d)

        keywords.append(list(output.values()))

def look_up(id,keywords):

    # Ignores case
    keywords = keywords.lower()

    for item in topics:

        # if any value contains s
        if any([keywords in v.lower() for v in item.values()]):
            # spit out the item — this is a generator function
            yield item

def search():

    flat_keywords_list = [item for sublist in keywords for item in sublist]

    for word in flat_keywords_list :

        query = word

        abc = []
        original = []
        choices = []

        # iterate over at most 500 first results (can be changed)
        for result in itertools.islice(look_up(abc,query),500):

            original.append(list(result.keys()))

            abc.append(list(result.items()))

            choices.append(list(result.values()))

        flat_list_1 = [item for sublist in choices for item in sublist]
        flat_list_2 = [item for sublist in original for item in sublist]

        # Compares keywords of each pbi vs original summary description
        # This gives a lower match score than comparing each pbi summary vs the other summaries

        output = process.extract(query,flat_list_1,scorer=fuzz.ratio,limit=1000)

        final = [tuple(j for j in i if not isinstance(j, str)) for i in output]

        zipped = [{"...:": list(zip(flat_list_2, final))}]

        print('')
        print('-' * 80)
        print('')

        flat_list_3 = [item for sublist in pbi for item in sublist]

        print('...: ' + query)

        print('')

        pprint.pprint(list(zip(flat_list_3, zipped)))

keyword_search()
search()