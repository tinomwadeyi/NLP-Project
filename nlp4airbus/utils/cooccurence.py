import itertools
import logging
from collections import Counter

import numpy as np
from scipy.sparse import csr_matrix, lil_matrix, triu, find
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import Binarizer


def create_co_occurences_matrix(documents, word_to_id):
    """
    Computes the co-occurences of words present in a corpus of documents

    :param documents: text
    :type documents: list of str
    :param word_to_id: maps a word to a unique identifier
    :type word_to_id: dict
    :return: matrix with the co-occurences of words (rows, cols are words and the values are co-occurences)
    :rtype: scipy.sparse.csr_matrix
    """
    # turn words to their id
    documents_as_ids = [np.sort([word_to_id[w] for w in doc.split(' ') if w in word_to_id]).astype('uint32')
                        for doc in documents]

    # get the row for unique doc and col for unique word
    row_ind, col_ind = zip(*itertools.chain(*[[(i, w) for w in doc] for i, doc in enumerate(documents_as_ids)]))

    # use unsigned int for better memory utilization
    data = np.ones(len(row_ind), dtype='uint32')
    max_word_id = len(word_to_id)

    # multiplying docs_words_matrix with its transpose matrix would generate the co-occurences matrix
    # efficient arithmetic operations with CSR * CSR
    docs_words_matrix = csr_matrix((data, (row_ind, col_ind)), shape=(len(documents_as_ids), max_word_id))
    words_cooc_matrix = docs_words_matrix.T * docs_words_matrix
    words_cooc_matrix.setdiag(0)

    return words_cooc_matrix


def cooccurences_words_per_class(corpus, labels, num_class, threshold=500, high_frequency=0.8):
    """
    In a classification, computes the most discriminative combination of words for each class

    :param corpus: documents containing string free text
    :type corpus: list of str
    :param labels: list of labels matching the documents in ``corpus``
    :type labels: list
    :param num_class: number of classes
    :type num_class: int
    :param threshold: keep the best cooccurences
    :type threshold: int
    :param high_frequency: threshold of occurences
    :type high_frequency: float

    :return: list of documents containing string free text with added new words coming from the disciminative
        combinations, list of unique words coming from the discrimination combinations of words
    """

    # get the vocabulary of the corpus
    tfidf_vec = TfidfVectorizer(stop_words='english', max_df=0.99, min_df=100)
    tfidf_vec.fit(corpus)
    voc = list(tfidf_vec.get_feature_names())
    logging.info("Vocabulary size of the corpus : {}".format(len(voc)))

    # create a sparse matrix full with 0 for each class
    l_mat = [lil_matrix((len(voc), len(voc))) for _ in range(num_class)]
    # create a sparse matrix full with 0 that will be the cooccurence matrix of the whole corpus
    big_mat = lil_matrix((len(voc), len(voc)))

    # dictionary that maps a word to an id
    word_to_id = dict(zip(voc, range(len(voc))))
    # dictionary that maps an id to a word
    id_to_word = dict(zip(range(len(voc)), voc))

    # compute cooccurence matrix for each class
    for cls in range(num_class):
        documents = [" ".join(list(set(doc.split(" ")))) for doc in [corpus[i] for i in np.where(labels == cls)[0]]]
        logging.info("label : {} - {} rows".format(cls, len(documents)))
        mat = create_co_occurences_matrix(documents, word_to_id)
        l_mat[cls] = mat

        # add the cooccurence of the curent class to the previous ones to get the total cooccurence through all classes
        big_mat += mat

    # apply a threshold : keep only the cooccurences being >= threshold in total and take the inverse element-wise
    big_mat_0 = Binarizer(threshold).fit_transform(big_mat)
    div_big_mat = big_mat.multiply(big_mat_0).power(-1)

    # apply multiplication between 2 matrices element-wise
    # thus, mat(i,j) becomes :
    # (cooccurence between word i and j in 'current class') / (cooccurence between word i and j in total)
    l_div_mat = []
    for cls in range(num_class):
        mat = l_mat[cls]
        mat = mat.multiply(div_big_mat)
        l_div_mat.append(mat)

    # filter on the most discriminative cooccurences
    dico_all = []
    # go throuh each class
    for cls in range(num_class):
        di = {'key': [], 'value': []}
        mat = l_div_mat[cls]
        # find all the cooccurences that have a high frequency in the class
        row_idx, col_idx, bins = find(np.all(triu(mat) > high_frequency))
        logging.info("nb obs : {}".format(row_idx.shape))
        logging.info("key")
        # map the ids back to their words
        key = [id_to_word[x] + " - " + id_to_word[col_idx[i]] for i, x in enumerate(row_idx)]
        logging.info("value")
        # get the value associated with the words
        value = [mat[x, col_idx[i]] for i, x in enumerate(row_idx)]
        di['key'] = key
        di['value'] = value
        dico_all.append(di)

    # put in vocab2 the unique words from all the combinations
    vocab2 = list(set([z for x in dico_all for y in x['key'] for z in y.split(' - ')]))

    # build a tfidf of these unique words
    tfidf_vec = TfidfVectorizer(stop_words='english', max_df=0.6, min_df=20, vocabulary=vocab2)
    tfidf = tfidf_vec.fit_transform(corpus)
    features = tfidf_vec.get_feature_names()
    logging.info("Vocabulary size of new vocabulary : {}".format(len(features)))

    # for each doc, extract the words containing in vocab2
    temp = [[features[y] for y in np.where(row.toarray().reshape(len(vocab2), ) > 0)[0]] for row in tfidf]

    # build a dictionary that maps a word to its associated co-occured words
    felement = np.array([y.split(' - ')[0] for x in dico_all for y in x['key']])
    selement = np.array([y.split(' - ')[1] for x in dico_all for y in x['key']])
    word_to_batch = {x: [selement[idx] for idx in np.where(felement == x)[0]] for x in vocab2}

    # go through the docs and check if a combination of words is found in dico_all
    # if so, add a new word (concatenation of both words) to the document
    logging.info("Final_docs")
    final_docs = [" ".join([word + "_" + w for i, word in enumerate(row) for w in row[i + 1:]
                            if w in word_to_batch[word]]) for row in temp]

    # get the new vocabulary
    new_vocabulary = [key + "_" + x for key in word_to_batch.keys() for x in word_to_batch[key]]
    logging.info("Vocabulary size of new vocabulary : {}".format(len(new_vocabulary)))

    return final_docs, new_vocabulary


def ratio_words_per_class(tfidf, features, labels, num_class, n=50, threshold=0.15):
    """
    In a classification, computes the most discriminative words per class.

    Pseudo-code:

    .. code::

        For each class, get the 'current class'
            For each class\{'current class'}, get the 'other class'
                For each feature,
                    - compute its ratio of occurence in docs of 'current class'.
                    - compute its ratio of occurence in docs of 'other class'.
                    - compute the difference between both ratios.
                Retrieve the features with the highest differences (those are discriminative features)

            For each feature,
                - compute the number of 'other class' that considered the feature discriminative
            Retrieve the features with the highest discriminative score (> threshold)

    :param tfidf: documents words matrix
    :param features: list of unique words coming from tfidf
    :param labels: list of labels matching the documents in ``corpus``
    :type labels: list
    :param num_class: number of classes
    :type num_class: int
    :param threshold: ratio threshold (keep above)
    :type threshold: float
    :param n: number of words to keep
    :type n: int

    :return: unique words that are the most discriminative
    :rtype: list of str
    """
    discriminative_words = []
    best_discriminative_words = []
    n2 = n
    for cls in range(num_class):

        logging.info("Class n° {} :".format(cls))
        logging.info("########################\n\n")

        idx_cls = (labels == cls)
        for cls2 in range(num_class):
            if cls2 == cls:
                continue

            idx_else = (labels == cls2)

            tfidf_cls = tfidf[idx_cls, :]
            tfidf_else = tfidf[idx_else, :]

            # associate each feature with its proportion of occurence in all the documents of 'current class'
            tf2 = np.array(np.sum(1 * (tfidf_cls > 0), axis=0) / tfidf_cls.shape[0]).reshape(tfidf_cls.shape[1], )
            # extract the n highest frequent features
            idx = tf2.argsort()[-n:][::-1]
            # associate each feature with its proportion of occurence in all the documents of 'other class'
            tf2_else = np.array(np.sum(1 * (tfidf_else > 0), axis=0) / tfidf_else.shape[0]).reshape(
                tfidf_else.shape[1], )

            # first, compute the difference between the frequency of occurence in docs of 'current class'
            # and the frequency of occurence in docs of 'other class'

            # then extract the highest differences
            sc = np.array([np.round(tf2[i] - tf2_else[i], 2) for i in idx if
                           ((tf2[i] - tf2_else[i] > threshold) or (tf2[i] >= 0.1 and tf2_else[i] < 0.02))])
            # then extract the frequencies of 'current class' with highest differences
            tv = np.array([np.round(tf2[i], 2) for i in idx if
                           ((tf2[i] - tf2_else[i] > threshold) or (tf2[i] >= 0.1 and tf2_else[i] < 0.02))])
            # then extract the frequencies of 'other class' with highest differences
            tv_else = np.array([np.round(tf2_else[i], 2) for i in idx if
                                ((tf2[i] - tf2_else[i] > threshold) or (tf2[i] >= 0.1 and tf2_else[i] < 0.02))])
            # then extract the features with highest differences
            ft = np.array([features[i] for i in idx if
                           ((tf2[i] - tf2_else[i] > threshold) or (tf2[i] >= 0.1 and tf2_else[i] < 0.02))])

            # store the features with highest differences
            discriminative_words.append(ft)
            logging.info("Class n° : {} with {} rows".format(cls2, tfidf_cls.shape[0]))
            logging.info(sc[sc.argsort()[-n2:][::-1]])
            logging.info(ft[sc.argsort()[-n2:][::-1]])
            logging.info(tv[sc.argsort()[-n2:][::-1]])
            logging.info(tv_else[sc.argsort()[-n2:][::-1]])
            logging.info("\n####")

        counter = Counter([y for x in discriminative_words for y in x]).most_common()
        logging.info(counter)

        # store the features that are the most discriminative across the other classes
        best_discriminative_words.append([tupple[0] for tupple in counter if tupple[1] >= 3])

    return best_discriminative_words


if __name__ == '__main__':
    import pandas as pd

    f = pd.read_csv('/Users/sicot/projets/embeddings/only_text_lr.csv').fillna('')
    f['all_text'] = f['snag_job_description'] + '. ' + f['snag_cor_action']
    docs = f['all_text'].tolist()

    tfidf_vec = TfidfVectorizer(stop_words='english', max_df=0.99, min_df=100)
    tfidf_vec.fit(docs)
    voc = list(tfidf_vec.get_feature_names())
    logging.info("Vocabulary size of the corpus : {}".format(len(voc)))
    word_to_id_test = dict(zip(voc, range(len(voc))))

    coomat = create_co_occurences_matrix(docs, word_to_id_test)
    coomat.shape
