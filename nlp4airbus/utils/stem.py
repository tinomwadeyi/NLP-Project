"""
This modules wrap NLTK stemmers and takes into acocunt Airbus vocabulary. It allows to use own stemmer.

.. note:: This module requires NLTK.
"""
import string

from nltk.stem import SnowballStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

from nlp4airbus.utils.lexinet import Lexinet


class Stem:
    """
    Stem either a single word or tokenize and stem a long text taking into account Airbus vocabulary.
    """

    #: list of words (acronyms) not to stem from :py:mod:`nlp4airbus.utils.lexinet`
    _no_stem = Lexinet().get_all_acronyms()
    _supported_languages = ['french', 'english', 'spanish', 'german']
    _snow_ball_stemmers = {lang: SnowballStemmer(lang) for lang in _supported_languages}

    def __init__(self, stemmer='SnowBall', language='english'):
        """
        :param stemmer: either a string for 'SnowBall' or an object with a ``stem`` method
        :type stemmer: str or object with ``stem`` method
        :param language: language of the text or ``'auto'``. The latter tries to detect the language of the text
           automatically. It should be one of the four languages of Airbus. If not, it defaults to english.
        :type language: str
        :raise: ValueError: when language is not supported
        """
        if language not in (self._supported_languages + ['auto']):
            raise ValueError('Language should be in %s' % self._supported_languages)

        self.language = language
        if stemmer == 'SnowBall':
            if language == 'auto':
                import langdetect
                self.stemmer = None
            else:
                self.stemmer = self._snow_ball_stemmers[language]
        else:
            self.stemmer = stemmer

    def stem_single_word(self, word):
        """
        Stem a single word

        :param word: token to stem
        :type word: str
        :return: stemmed word
        :rtype: str

        >>> from nlp4airbus.utils.stem import Stem
        >>> s = Stem()
        >>> s.stem_single_word('Brakes')
        'brake'
        >>> s.stem_single_word('ACMS')
        'ACMS'
        """
        if word.lower() in self._no_stem:
            return word
        else:
            return self.stemmer.stem(word)

    def tokenize_and_stem_long_text(self, text, output='string', remove_punctuations=True):
        """
        Stem a long text. Perform tokenization on the fly.

        :param text: token to stem
        :type text: str
        :param output: Kind of output (either ``'tokens'`` for list of tokens or ``'string'`` for a string of stemmed
            tokens separated by a single space)
        :type output: str
        :param remove_punctuations: remove puncutation from output
        :type remove_punctuations: bool
        :return: a list or a string of stemmed tokens
        :type: list of str or str

        :raises: ValueError: when output type is not known

        >>> from nlp4airbus.utils.stem import Stem
        >>> s = Stem()
        >>> s.tokenize_and_stem_long_text('As Level Sense Test OK TSD Shows this as a Spurious Indication, associated with power switching, displayed at Engine Start which is a known issue. ')
        'As level sens test OK TSD show this as a spurious indic associ with power switch display at engin start which is a known issu'
       """

        if output not in ['tokens', 'string']:
            raise ValueError("Output must be in ['tokens', 'string']")

        # tokenize sentences and words. Then apply stemmer if token not in Airbus acronyms
        stemmed_tokens = []
        if self.language == 'auto':
            from langdetect import detect
            cur_language = detect(text)
            if cur_language == 'fr':
                cur_language = 'french'
            elif cur_language == 'es':
                cur_language = 'spanish'
            elif cur_language == 'de':
                cur_language = 'german'
            else:
                cur_language = 'english'
            cur_stemmer = self.snow_ball_stemmers[cur_language]
        else:
            cur_language = self.language
            cur_stemmer = self.stemmer

        for sentence in sent_tokenize(text, language=cur_language):
            for word in word_tokenize(sentence, language=cur_language):
                if word.lower() not in self._no_stem:
                    stemmed_tokens.append(cur_stemmer.stem(word))
                else:
                    stemmed_tokens.append(word)

        # remove punctuation tokens
        if remove_punctuations:
            stemmed_tokens = [t for t in stemmed_tokens if t not in string.punctuation]

        if output == 'tokens':
            return stemmed_tokens
        elif output == 'string':
            return ' '.join(stemmed_tokens)


if __name__ == '__main__':

    # import doctest
    # doctest.testmod()

    s = Stem()
    print(s.stem_single_word('Brakes'))
    print(s.stem_single_word('ACMS'))
    print(s.tokenize_and_stem_long_text('As Level Sense Test OK TSD Shows this as a Spurious Indication, associated with power switching, displayed at Engine Start which is a known issue. '))
    print(s.tokenize_and_stem_long_text('Bite test of CDSS performed IAW AMM task 23-72-00-710-801 work performed by david Sanz'))
