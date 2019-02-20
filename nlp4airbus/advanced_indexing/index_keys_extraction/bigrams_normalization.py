"""
Created on 06/06/2018
@author: David ROUSSEL

This is a set of functions to normalize bigrams, i.e. filter the forms that only convey noise or undesired content (e.g. person names)
After spelling correction, words of frequence 1 are supposed to be corrected.
After decomposition of NE or NP into bigrams, there are still different variants such as:
* word inversions: 'HARD_LANDING', 'LANDING_HARD'
* mistakes
* inflections
* abbrev : 'DAILY_CHECK', 'DAILY_CHK'
Following code is useful to normalize the bigrams of freq > 1

"""
import nltk
from gensim.parsing.preprocessing import strip_punctuation
#from linguistic_resources import ListStopWordsUpper, ListStopWordsOrAntidico
from nlp4airbus.advanced_indexing.index_keys_extraction.linguistic_resources import ListStopWordsUpper, ListStopWordsOrAntidico
import re


def filter_punk(merged_bigrams):
    return [[strip_punctuation(word) for word in ng] for ng in merged_bigrams]


def filter_stopWords(merged_bigrams, sw=ListStopWordsUpper):
    '''filter out bigram according a list of stop words'''
    filtered_ngrams = [wrd for wrd in merged_bigrams if (frozenset(sw).isdisjoint(wrd.split(' ')))]
    return filtered_ngrams


def filter_stopWordsOrAntidico(merged_bigrams, sw=ListStopWordsOrAntidico):
    '''filter out bigram according a list of stop words and an antidico for technical designations'''
    filtered_ngrams = [wrd for wrd in merged_bigrams if (frozenset(sw).isdisjoint(wrd.split(' ')))]
    return filtered_ngrams


def filter_firstNames(merged_bigrams, names):
    filtered_ngrams = [wrd for wrd in merged_bigrams if not_person_name(wrd.split(' '), names)]
    return filtered_ngrams


def filter_firstNames_p27(merged_bigrams, names):
    filtered_ngrams = [wrd for wrd in merged_bigrams if not_person_name_p27(wrd.split(' '), names)]
    return filtered_ngrams


def init_filter_firstNames_p27():
    '''NLTK comes with resources female.txt and male.txt, each containing 
    a list of a few thousand common first names.
    It is relevant to filter out potential person names from a list of keywords.
    the p27 release loads the file using the load function.'''

    path = "nltk:names/male.txt"

    try:
        first_names = nltk.data.load(path)
        return first_names

    except:
        print ("Error on nltk person names loading")
        return []


def init_filter_firstNames():
    '''NLTK comes with resources female.txt and male.txt, each containing 
    a list of a few thousand common first names.
    It is relevant to filter out potential person names from a list of keywords.
    this release loads the file using the names function.'''
    from nltk.corpus import names
    try:
        first_names = names.words('male.txt')
        return first_names
    except:
        print ("Error on nltk person names loading")
        return []


def not_person_name(ngram, first_names):
    '''compare ngram string converted into a first letter capitalized string
    with the list of first names'''
    for wd in ngram:
        if wd.title() not in first_names:
            return True

    return False


def not_person_name_p27(ngram, first_names):
    res = True
    for wd in ngram:
        if first_names.find(wd.title()) != -1:
            return False
    return res


def shortenChunks(chunks, ListStopWordsUpper_regexp):
    """shorten some chunks by filtering the stopWords in.
    ListStopWordsUpper_regexp can be ListStopWordsUpperNotInNP"""
    shortened = [[re.sub(ListStopWordsUpper_regexp, '', wrd.upper()).strip() for wrd in text] for text in chunks]

    return shortened
