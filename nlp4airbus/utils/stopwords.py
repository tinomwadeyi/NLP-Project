"""
This class allows to construct a domain specific stop words list based on word frequency and inverse-document
frequency (the IDF of TF-IDF). There are 3 tunable criteria.

#. Most frequent words: remove words that appears very often in the corpus.
   Can be an absolute count or a document proportion

#. least common words: remove words that are very rarely used and add noise to the text. There can be a lot of
   regular but misspelled words.

#. words with low inverse document frequency (IDF). The inverse document frequency is a measure of how much
   information the word provides, that is, whether the term is common or rare across all documents.
   It is the logarithmically scaled inverse fraction of the documents that contain the word, obtained by dividing
   the total number of documents by the number of documents containing the term, and then taking the logarithm
   of that quotient.

The implementation is based on scikit-learn `TF-IDF vectorizer
<http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html>`_.

Example
-------

.. code:: python

    import pandas as pd

    from nlp4airbus.utils.stopwords import Stopwords

    f = pd.read_csv('etlb.csv').fillna('')
    f['all_text'] = f['snag_job_description'] + '. ' + f['snag_cor_action']
    docs = f['all_text'].tolist()
    sw = Stopwords(docs)
    most_ccmmon = sw.get_most_common_stopwords(0.25)
    # ['flight', 'stamp', 'crew', 'evrt', 'performed', 'sub', 'final', 'perform', 'please', 'task', 'item', 'stamped',
    # 'changed', 'accept', 'iaw

.. note:: This module requires NLTK and Scikit-Learn.

.. todo:: move from sklearn to gensim to reduce package dependency

"""
import re

import numpy as np
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

from nlp4airbus.utils.substitution import Substitutions


class Stopwords:

    _lang_stopwords = {'english': set(stopwords.words('english')),
                       'french': set(stopwords.words('french')),
                       'spanish': set(stopwords.words('spanish')),
                       'german': set(stopwords.words('german'))}

    def __init__(self, documents, language='english', stem=False, only_alpha=True):
        """

        :param documents: list of documents
        :param language: choose among ['english', 'french', 'spanish', 'german']
        :param stem: whether words are stemmed or not
        :param only_alpha: if True, only keep stopwords with alphabetic characters (not numerical)
        """
        self.corpora = documents
        self.stem = stem
        self.language = language
        self.only_alpha = only_alpha

    def get_stopwords(self, min_df=2, max_df=0.25, min_tfidf='outliers'):
        """

        Get the list of stopwords satisfying given parameetrs.

        :param min_df: ignore terms that have a document frequency strictly lower than the given threshold.
            This value is also called cut-off in the literature. If float, the parameter represents a proportion
            of documents, integer absolute counts.
        :type min_df: integer or float
        :param max_df: gnore terms that have a document frequency strictly higher than the given threshold .
            If float, the parameter represents a proportion of documents, integer absolute counts.
        :type max_df: integer or float
        :param min_tfidf: if set to ``'outliers'`` remove terms that are in the lower tail of IDF distribution.
            If float, remove terms that are below the given threshold.
        :type min_tfidf: str or float
        :type min_tfidf: str or float
        :return: list of stopwords
        :rtype: list of str
        """
        tfidf_vec = TfidfVectorizer(min_df=min_df, max_df=max_df,
                                    stop_words=self._lang_stopwords[self.language])
        tfidf_vec.fit(self.corpora)
        tfidf_stopwords = list(tfidf_vec.stop_words_)

        # remove words with low TF-IDF
        bplt = None
        if isinstance(min_tfidf, str):
            if min_tfidf == 'outliers':
                q25, q75 = np.percentile(tfidf_vec.idf_, 25), np.percentile(tfidf_vec.idf_, 75)
                iq = q75 - q25
                bplt = q25 - 1.5 * iq
        elif isinstance(min_tfidf, float):
            bplt = min_tfidf

        if bplt is not None:
            for token, idf in zip(tfidf_vec.get_feature_names(), tfidf_vec.idf_):
                if idf < bplt:
                    tfidf_stopwords.append(token)

        # remove tokens that are not words
        if self.only_alpha:
            tfidf_stopwords = list(filter(lambda s: s.isalpha(), tfidf_stopwords))

        return tfidf_stopwords

    def get_most_common_stopwords(self, max_df=0.4):
        """
        Get stopwords that are too frequent in the corpus

        :param max_df: When building the vocabulary ignore terms that have a document frequency strictly higher than
            the given threshold (corpus-specific stop words). If float, the parameter represents a proportion of
            documents, integer absolute counts.
        :type max_df: integer or float
        :return: list of most common stopwords
        :rtype: list of str
        """
        return self.get_stopwords(min_df=1, max_df=max_df, min_tfidf=None)

    def get_least_common_stopwords(self, min_df=2):
        """
        Get stopwords that are too rare in the corpus

        :param min_df: ignore terms that have a document frequency strictly lower than the given threshold.
            This value is also called cut-off in the literature. If float, the parameter represents a proportion
            of documents, integer absolute counts.
        :type min_df: integer or float
        :return: list of least common stopwords
        :rtype: list of str
        """
        return self.get_stopwords(min_df=min_df, max_df=1.0, min_tfidf=None)

    def remove_stop_words(self, stopwords_list, replacement=' ', include_lang_stopwords=True):
        """
        Remove stopwords from corpus

        :param stopwords_list: list of stopwords
        :type: list
        :param replacement: string replacement for each stopword
        :type replacement: str
        :param include_lang_stopwords: add language stopwords to the given list
        :type include_lang_stopwords: bool
        :return: corpus with stopwords replaced
        """

        if include_lang_stopwords:
            stopwords_list += self._lang_stopwords[self.language]
        s = Substitutions({k: replacement for k in stopwords_list})
        return map(lambda txt: re.sub(r'\s+', ' ', (s.substitute(txt))), self.corpora)


if __name__ == '__main__':
    import pandas as pd
    from nlp4airbus.re.clean import Cleaner

    f = pd.read_csv('/Users/sicot/projets/embeddings/only_text_lr.csv', nrows=1000).fillna('')
    f['all_text'] = f['snag_job_description'] + '. ' + f['snag_cor_action']
    # docs = [lorem.sentence() for _ in range(10)]
    docs = f['all_text'].tolist()
    sw = Stopwords(docs)
    most_Common = sw.get_most_common_stopwords(0.2)
    least_common = sw.get_least_common_stopwords(2)
    sw.get_stopwords(2, 0.4)

    idx = 109

    c = Cleaner()
    f['snag_cor_action_clean'] = f['snag_cor_action'].map(c.clean)

    sw = Stopwords(f['snag_cor_action_clean'])
    most_common_in_tlb = sw.get_most_common_stopwords(0.25)
    f['snag_cor_action_clean_no_stop'] = list(sw.remove_stop_words(most_common_in_tlb))
    f.head()
