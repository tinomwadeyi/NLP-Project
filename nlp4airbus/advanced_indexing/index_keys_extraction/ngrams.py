"""
Created on 06/06/2018
@author: David ROUSSEL

Multigram computation algorithms from nltk package implementation.
Heuristics have been implemented to extract each uppercase from titles except if the number of known acceptions is huge.
"""
import nltk
from nltk.corpus import wordnet as wn
from nlp4airbus.advanced_indexing.index_keys_extraction.linguistic_resources import ListStopWordsOrAntidico
import re
from collections import Counter
from math import log


def createAcronymOrMultiGramFromText(x, min_len, ngram=None, sep=' '):
    try:
        sentences = list(map(unicode.strip, x.upper().split(sep)))
        if ngram == None:
            max_ngram = len(sentences) -1
        else:
            max_ngram = ngram
        res = list(nltk.everygrams(sentences, min_len=min_len, max_len=max_ngram))
    except:
        res = None
        pass
    if(not(x.islower() and x.isupper())):
        c = re.compile(r"\b[A-Z]+\b")
        substrings = c.findall(x)
        for s in substrings:
                res.append([s]);
    print(res)
    res2 = [' '.join(res_i) for res_i in res]
    return res2


def heuristicNgramsFromTitle(x, min_len, ngram=None, _heuristic_max_length=2, sep=' '):
    '''use of wordnet synset to check if the upper case isolated word is very common.
    Also filter out supposed acronyms of length 2'''
    sentences = list(map(str.strip, x.upper().split(sep)))
    if(len(sentences) < _heuristic_max_length): return []
    try:
        if ngram == None:
            max_ngram = len(sentences) -1
        else:
            max_ngram = ngram   
        res = list(nltk.everygrams(sentences, min_len=min_len, max_len=max_ngram))
    except:
        res = []
        pass
    if(not(x.islower() and x.isupper())):
        # get the bigrams if at least one word is uppercase
        c=re.compile(r"^([A-Z]+)\b|[\.a-z]+\s+\b([A-Z]+)\b\s*[\.a-z]+")
        substrings = c.findall(x)
        for s in substrings:
            theString = str.strip(' '.join(s))
            if(len(wn.synsets(theString)) < 5):
                res.insert(0,s);
            #else: print(wn.synsets(theString))
    res2 = [str.strip(' '.join(res_i)) for res_i in res if ((not (res_i[0] in ListStopWordsOrAntidico)) and (not (res_i[1] in ListStopWordsOrAntidico)))]
#    res2 = [str.strip(' '.join(res_i)) for res_i in res if not((res_i[0] in ListStopWordsOrAntidico) or (res_i[1] in ListStopWordsOrAntidico))]
    return [x for x in res2 if len(x) > 2]


def createMultiGramFromText(x, min_len, ngram=None, sep=' '):
    try:
        sentences = list(map(unicode.strip, x.split(sep)))
        if ngram == None:
            max_ngram = len(sentences) - 1
        else:
            max_ngram = ngram
        res = nltk.everygrams(sentences, min_len=min_len, max_len=max_ngram)

    except:
        res = None
        pass
    res1 = list(res)
    res2 = [' '.join(res_i) for res_i in res1]
    return res2


def createBigramsFromNGrams(array, sep=' '):
    '''to recreate bigrams in upper case from longer ngrams'''
    res=[]
    for x in array:
        sentences = list(map(unicode.strip, x.upper().split(sep)))
        if len(sentences) == 1:
            res.append(sentences)
        else:
            res.extend(nltk.everygrams(sentences, min_len=2, max_len=2))

    return [' '.join(res_i) for res_i in list(res)]



def controled_indexing_uniq(text,ngram_set,ngram_maxsize=2):
    '''find ngrams of a given set that are contained in a text'''
    #too permissive [word for word in keyword_list if word in all_text_words ]
    all_ngrams = createMultiGramFromText(text.upper(), 1, ngram_maxsize, sep=None)
    return ngram_set.intersection(all_ngrams)    

def controled_indexing(text,ngram_set,ngram_maxsize=2):
    '''find ngrams of a given set that are contained in a text'''
    #too permissive [word for word in keyword_list if word in all_text_words ]
    all_ngrams = createMultiGramFromText(text.upper(), 1, ngram_maxsize, sep=None)
    return [x for x in all_ngrams if x in ngram_set]


def gen_bigrams(data, window_size=5):
    for idx in range(len(data)):
        window = data[idx: idx + window_size]

        if len(window) < 2:
            break

        w = window[0]
        for next_word in window[1:]:
            yield (w, next_word)

def construct_vocab(data):
    vocab = Counter()
    for (w1, w2) in gen_bigrams(data, window_size=3): # count 1gram & 2gram
        vocab.update([w1, w2, (w1, w2)])
    return vocab

def calc_pmi(vocab):
    det = sum(vocab.values())
    for (w1, w2) in filter(lambda el: isinstance(el, tuple), vocab):
        p_a, p_b = float(vocab[w1]), float(vocab[w2])
        p_ab = float(vocab[(w1, w2)])

        yield (w1, w2, log((det * p_ab) / (p_a * p_b), 2))
