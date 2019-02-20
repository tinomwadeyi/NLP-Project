from collections import Counter

import nltk


def create_multi_gram_from_text(text, min_len, ngram=None, sep='_'):
    """
    create multi-gram from text

    :param text: string
    :param min_len: minimum length
    :param ngram: maximum length
    :param sep: separator of tokens in the grams
    :return: list of ngrams

    .. warning:: Take care following code does not preserve the word order. See advanced indexing functions for this

    """
    try:
        sentences = text.split(' ')
        # todo: sentences = list(map(unicode.strip, text.split(sep)))

        if ngram is None:
            max_ngram = len(sentences) - 1
        else:
            max_ngram = ngram
        res = nltk.everygrams(sentences, min_len=min_len, max_len=max_ngram)

    except:
        res = None
        pass

    # res1 = list(Counter(res)) deduplicate !
    res1 = list(res)
    res2 = [' '.join(res_i) for res_i in res1]
    return res2


def create_bigram_from_noun_phrases(array):
    """
    generate bigrams. deprecated.
    """
    return createBigramsFromNGrams(array, sep=' ', outsep=' ')


def createBigramsFromNGrams(array, sep=' ', outsep=' '):
    """to recreate bigrams in upper case from longer ngrams
    :param array: array of ngrams
    :param sep: seperator used in original list
    :param outsep: seperator used in output list
    :return:
    """
    res = []
    for x in array:
        sentences = list(map(unicode.strip, x.upper().split(sep)))
        if len(sentences) == 1:
            res.append(sentences)
        else:
            res.extend(nltk.everygrams(sentences, min_len=2, max_len=2))

    return [outsep.join(res_i) for res_i in list(res)]
