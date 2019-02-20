"""
Created on 06/06/2018
@author: David ROUSSEL

Ngrams substitution utils, inluding creation and substitution.
"""
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
from fuzzywuzzy import utils
import hashlib
from functools import partial

from collections import defaultdict
import itertools
import csv
#import codecs
import pandas as pd
import pickle
import os
import numpy as np

def frequent_ngrams(pd_serie, cutter=2):
    '''generate the list of frequent bigrams (or any ngrams) in upper case from a pandas series'''
    frequency = ngram_frequency(pd_serie)
    frequent_bigrams = [[token for token in text if frequency[token] >= cutter] for text in pd_serie.dropna().values]
    return list(set(itertools.chain.from_iterable(frequent_bigrams)))


def ngrams_longer_than(ngrams_list, cutter):
    '''generate the list of bigrams longer than the cutter'''
    return [token for token in ngrams_list if len(token) > cutter]


def ngram_frequency(pd_serie):
    frequency = defaultdict(int)
    print(pd_serie.values)
    for ngram in pd_serie.values:
        try:
            for token in ngram:
                frequency[token] += 1
        except TypeError:
            pass
    return frequency


def test_similarities(names, scorer, cut, frequency):
    '''simplification of test_similarities_by_score. It add a prefilter on the frequency if not already done'''
    clusters = {}
    fuzzed = []

    for t in names:
            if(frequency[t] > 2):
                fuzzyset = process.extractBests(t, names, scorer=scorer, score_cutoff=cut)
                # Generate a key based on the sorted members of the set
                keyvals = sorted(set([x[0] for x in fuzzyset]), key=lambda x: names.index(x), reverse=False)

                keytxt = ' '.join(keyvals)
                key = keytxt

            if len(keyvals) > 1 and key not in fuzzed:
                clusters[key] = sorted(set([x for x in fuzzyset]), key=lambda x: frequency[x[0]], reverse=True)
                fuzzed.append(key)
    return clusters


def test_similarities_by_score(names, scorer, cut, verbose=False):
    '''This function compute potential substitution to apply.
    The Partial_ratio scorer returns the ratio of the most similar substring using the shortest 
    string (length n) against all n-length substrings of the larger string and returns the highest score.
    the UWRATIO method returns a measure of the sequences using different algorithms. 
    UWRATIO is same as WRatio but preserving unicode
    '''
    clusters = {}
    fuzzed = []
    i = 0
    j = 0

    for t in names:
        j = j + 1
        if verbose and (j % 50 == 0): 
            print("\nProcess ")
            print(names[i:j])
            i = j

        fuzzyset = process.extractBests(t, names, scorer=scorer, score_cutoff=cut)
        # Generate a key based on the sorted members of the set
        keyvals = sorted(set([x[0] for x in fuzzyset]), key=lambda x: names.index(x), reverse=False)

        keytxt = ' '.join(keyvals)
        key = keytxt

        if len(keyvals) > 1 and key not in fuzzed:
            clusters[key] = sorted(set([x for x in fuzzyset]), key=lambda x: x[1], reverse=True)
            fuzzed.append(key)
    return clusters


def save_variants_as_csv(mydict, TEMP_FOLDER='./'):
    filename = TEMP_FOLDER + "bigrams_variants_" + str(len(mydict)) + ".csv"

#    with codecs.open(filename, encoding='utf8', mode='w') as f_out:
    with open(filename, encoding='utf8', mode='w') as f_out:

        header = ['From', 'To']
        # set up csv reader and writer objects

        w = csv.writer(f_out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(header)
        w.writerows(mydict.items())
        f_out.close()


def substs_startingwith(astr, variants):
    '''astr is a string; variants is a 2 columns dict'''
    for fromw, tow in variants.items():
        if tow.startswith(astr):
            print (fromw, tow)


def init_variants(candidat_ngrams, variants, sep=';', verbose=False):
    '''init the substitution table from a previous result that is supposed to be validated (Status=1)
    use a null filename to regenerate a subtitution table automatically'''

    # variants = []

    # try:
    #     variants = pd.read_csv(filename, sep=sep).dropna()
    # except:
    #     print(filename + ' variants not found\n')

    if variants.shape[0] > 0:
        # errors with following code
        # dd = defaultdict(str)
        # variants2 = variants.to_dict(orient='records',into=dd)

        variants2 = defaultdict(str)

        for _, x in variants.iterrows():
            variants2[x['From']] = x['To'] 

    elif len(variants) <= 0:
        clusters = test_similarities_by_score(candidat_ngrams, fuzz.UWRatio, 86, verbose)
        if(verbose):
            print(str(len(clusters)) + " similarities between bigrams found")
        # chosen order = from -> to
        # test score between the most frequent words aligned 
        # eliminate repetitions because it biases the score, 
        # note revision should be done afterwards. 
        variants2 = defaultdict(str)

        for w in clusters.values():
            words = w[0][0].split(' ')
            if(len(words) > 1):
                if (words[0] != words[1]): 
                    for i in range(1, len(w)):
                        if ((w[0][1] >= 87) & (w[i][1] >= 88)):
                            # eliminate reverse substitution suggestion
                            if(not (w[i][0] in variants2 and w[0][0] == variants2[w[i][0]])):
                                words = w[i][0].split(' ')
                                if(len(words) > 1):
                                    # eliminate revision
                                    if (not(words[0] == words[1])):
                                        variants2[w[i][0]] = w[0][0]
                                else:
                                    variants2[w[i][0]] = w[0][0]
                            else:
                                print("reverse")

        # save_path = filename[:filename.rfind("/") + 1]
        # save_variants_as_csv(variants2, TEMP_FOLDER=save_path)
        # if(verbose):
        # print("Filtered variants saved under " + save_path + "bigrams_variants_" + str(len(variants2)))
    return variants2


def save_variants(variants, TEMP_FOLDER='./'):
    '''
    This method locally saves pickle file of variants. Each file is prefixed by bigrams_variants_ followed by the number of variants
    '''
    filename = TEMP_FOLDER + "bigrams_variants_" + str(len(variants)) + ".pickle"
    with open(filename, 'wb') as handle:
        pickle.dump(variants, handle, protocol=pickle.HIGHEST_PROTOCOL)


def load_variants():
    '''
    This method loads local pickle file of variants. Each file is supposed to start with bigrams_variants_
    '''

    # todo: filename from TEMP_FOLDER  ?
    file_list = os.listdir(".")
    
    for file in file_list:
        if (file.endswith(".pickle") & file.startswith("bigrams_variants_")):
            filename = file
    file = open(filename, 'rb')
    data_dict = pickle.load(file)
    file.close()
    return data_dict 



def apply_replacements(ngrams, vref):
    '''
    Subsitute any ngrams of a list with a normalized form taking the last pair of a managed list of variants
    :ngrams ngrams_list: list of ngrams
    :vref list of variants. Using a dict would improve the performances. If needed, use utils.substitution package instead of this function
    :return: list of normalized ngrams 
    '''
    finaltexts = []

    words = []
    try:
            for word in ngrams:
                test=vref[vref.FROM_VALUE == word].values
                if (len(test) > 0):
                    words.append(test[len(test)-1][1])
                else:
                    words.append(word)
            finaltexts.append(words)
    except TypeError:
            finaltexts.append(words)
    return finaltexts