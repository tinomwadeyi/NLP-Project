"""
This is a substitution class to replace words based on a dictionary of words to replace with corresponding
replacement words. A dictionary provided by SBO3 (Fabrice Ladchurie) is available in the package.

There are 2 substitution algorithm:

#. a naive implementation that loop over the whole dictionnary and test if the word replace belongs to the string
#. `FlashText <https://github.com/vi3k6i5/flashtext>`_ which use a
   `trie <https://en.wikipedia.org/wiki/Trie>`_ to better search for token in text

Flashtext being only available through pip and not Anaconda, it is not available on Skywise Foundry. It is therefore
shipped in the current package at :py:mod:`nlp4airbus.external.flashtext`.

FlashText is much faster:

.. code:: python

    import pandas as pd
    from nlp4airbus.utils.substitution import Substitutions
    from timeit import default_timer as timer

    f = pd.read_csv('/Users/sicot/projets/embeddings/only_text_lr.csv').fillna('').head(1000)
    f['all_text'] = f['snag_job_description'] + '. ' + f['snag_cor_action']

    sflashtext = Substitutions()
    snaive = Substitutions(algo='naive')

    start_flashtext = timer()
    f['all_text_clean_flashtext'] = f['all_text'].map(sflashtext.substitute)
    end_flashtext = timer()
    flashtext_duration = end_flashtext - start_flashtext

    start_naive = timer()
    f['all_text_clean_naive'] = f['all_text'].map(snaive.substitute)
    end_naive = timer()
    naive_duration = end_naive - start_naive

    # -> Naive duration 408.283s, FlashText duration: 0.347s (1178.08x faster)

.. note:: This module requires Pandas. It is also recommended to have FlashText installed although a dump is provided as
          a module in :py:mod:`nlp4airbus.external.flashtext`.
"""

import os.path as pa
import re

import pandas as pd
from nltk.corpus import stopwords


class Substitutions:
    """
    Substitution class
    """

    def __init__(self, substitution_dict='SBO3', algo='flashtext', case_sensitive=False):
        """
        :param substitution_dict: either a

            * dictionary of original/replacement strings
            * a string among
                * ``'SBO3'`` is the default dictionary provided by Fabrice Ladchurie (SBO3). Based on Operational
                  Interruptions.
                * ``'lexinet'`` expand Airbus Acronyms with their long form (duplicated acronyms are ignored)

        :param algo: Algorithm to perform the text replacement:

            * ``'flashtext'``: subtitute text with `flashtext <https://github.com/vi3k6i5/flashtext>`_ module
            * ``'naive'``: use naive loops

        :raise ValueError: if unknown dictionary or unknown substitution algorithm
        """

        # get lower case dictionary
        self.case_sensitive = case_sensitive

        if isinstance(substitution_dict, dict):
            subst_dict = substitution_dict
        elif isinstance(substitution_dict, str):
            if substitution_dict == 'SBO3':
                subst_dict = (pd.read_csv(pa.join(pa.dirname(pa.abspath(__file__)),
                                          '..', 'data', 'substitution_SBO3.csv.gz'), sep=';').dropna()
                              .set_index('FROM_VALUE').squeeze().to_dict())
            elif substitution_dict == 'lexinet':
                subst_df = (pd.read_csv(pa.join(pa.dirname(pa.abspath(__file__)),
                                        '..', 'data', 'lexinet_acronyms.csv.gz'))
                            .dropna())
                # remove acronyms that are also stopwords
                en_stopwords = set(stopwords.words('english'))
                subst_df = subst_df[~subst_df['Abbr'].str.lower().isin(en_stopwords)]

                all_acronyms = set(subst_df['Abbr'].tolist())

                subst_df_noduplicates = subst_df.drop_duplicates(subset='Abbr', keep=False)
                single_acronyms = set(subst_df_noduplicates['Abbr'].tolist())

                acronyms_several_meaning = all_acronyms.difference(single_acronyms)

                subst_dict = subst_df_noduplicates.set_index('Abbr')['Full Form'].squeeze().to_dict()
            else:
                raise ValueError('Unknwon dictionary')

        # convert all to lower case if needed
        if case_sensitive:
            self.subst_dict = subst_dict
        else:
            self.subst_dict = {}
            for k, v in subst_dict.items():
                self.subst_dict[k.lower()] = v.lower()

        # if flashtext, test if module can be imported
        if algo == 'flashtext':
            try:  # try system-wide package
                from flashtext import KeywordProcessor
                self.algo = 'flashtext'
                self.keyword_processor = KeywordProcessor(case_sensitive=self.case_sensitive)
                for k, v in self.subst_dict.items():
                    self.keyword_processor.add_keyword(k, v)
            except ImportError:
                try:  # try embedded external module
                    from nlp4airbus.external.flashtext import KeywordProcessor
                    self.algo = 'flashtext'
                    self.keyword_processor = KeywordProcessor(case_sensitive=self.case_sensitive)
                    for k, v in self.subst_dict.items():
                        self.keyword_processor.add_keyword(k, v)
                except Exception:  # else go for naive algorithm
                    self.algo = 'naive'
        elif algo == 'naive':
            self.algo = 'naive'
        else:
            raise KeyError('Unknwon substitution algorithm')

    def __substitute_flashtext(self, text):
        """
        subtitute text with `flashtext <https://github.com/vi3k6i5/flashtext>` module

        :param text: text to substitute
        :return: substituted text
        """
        return self.keyword_processor.replace_keywords(text)

    def __subtitute_naive(self, text):
        """
        substitute text with regex

        :param text: text to substitute
        :return: substituted text
        """

        if not self.case_sensitive:
            text = text.lower()

        for k, v in self.subst_dict.items():

            v2use = v.replace('-', '')

            if k == v2use:
                continue

            if isinstance(k, str):
                if len(k.split()) > 1:
                    continue

            if isinstance(k, float):
                continue

            if len(k) == 1:
                continue
            if (len(k) == 2) and (k == v.replace(' ', '')):
                continue

            text = re.sub(r'\b%s\b' % re.escape(k), v, text)

        return text

    def substitute(self, text):
        """
        Replace text with dictionary substitution

        :param text: original text
        :type text: str
        :return: text with replacement
        :rtype: str

        >>> from nlp4airbus.utils.substitution import Substitutions
        >>> s = Substitutions()
        >>> s.substitute("PRODUCTION ITEM: Cabin, Area 2 RH, frame 37.1-37.2, dado panel item 203, P/N G252.88314.021 is not correctly cutted. AM reject N? 9177299 for the panel.")
        'PRODUCTION ITEM: Cabin, Area 2 right, frame 37.1-37.2, dado panel item 203, part number G252.88314.021 is not correctly cutted. AM reject N? 9177299 for the panel.'
        >>> slex =  Substitutions(substitution_dict='lexinet')
        >>> slex.substitute("Bite test of CDSS performed IAW AMM task 23-72-00-710-801 work performed by #person")
        'built-in test equipment test of cockpit door surveillance system performed in accordance with AMM task 23-72-00-710-801 work performed by #person'
        """
        if self.algo == 'flashtext':
            return self.__substitute_flashtext(text)
        else:
            return self.__subtitute_naive(text)


if __name__ == '__main__':

    f = pd.read_csv('/Users/sicot/projets/NLP/embeddings/only_text_lr.csv').fillna('').head(1000)
    f['all_text'] = f['snag_job_description'] + '. ' + f['snag_cor_action']

    sflashtext = Substitutions(substitution_dict='lexinet')
    textex = "The A/C CIDS is ABN"
    print(textex)
    print(sflashtext.substitute(textex))

    textex = 'Bite test of CDSS performed IAW AMM task 23-72-00-710-801 work performed by #person'
    print(textex)
    print(sflashtext.substitute(textex))

    # benchmark
    # from nlp4airbus.utils.substitution import Substitutions
    # from timeit import default_timer as timer
    #
    # sflashtext = Substitutions()
    # snaive = Substitutions(algo='naive')
    #
    # start_flashtext = timer()
    # f['all_text_clean_flashtext'] = f['all_text'].map(sflashtext.substitute)
    # end_flashtext = timer()
    # flashtext_duration = end_flashtext - start_flashtext
    #
    # start_naive = timer()
    # f['all_text_clean_naive'] = f['all_text'].map(snaive.substitute)
    # end_naive = timer()
    # naive_duration = end_naive - start_naive
    #
    # print('Naive duration %.3fs, FlashText duration: %.3fs (%.2fx faster)' % (naive_duration, flashtext_duration,
    #                                                                           naive_duration / flashtext_duration))
