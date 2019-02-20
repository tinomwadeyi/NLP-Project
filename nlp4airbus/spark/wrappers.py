"""This module implement function to create Spark User-Defined Functions (UDF) as wrappers to ``nlp4airbus``
functions.

These UDF performs type checks, create ``nlp4airbus`` objects and wrap their methods.
"""

import six

try:
    from pyspark.sql.types import StringType
    import pyspark.sql.functions as F
except ImportError:
    print('Spark not avaialble')

import nlp4airbus.re.clean as nlp4airbus_cleaner
import nlp4airbus.utils.substitution as nlp4airbus_subst
import nlp4airbus.utils.stem as nlp4airbus_stem
import nlp4airbus.utils.encoding as nlp4airbus_encoding
import nlp4airbus.utils.distances as nlp4airbus_dist


# cleaner
def create_udf_cleaner():
    """
    Create a text cleaner UDF

    :return: Spark UDF to clean a Spark dataframe column
    """
    c = nlp4airbus_cleaner.Cleaner()

    def clean_text(text):
        if text is None:
            return
        if not (isinstance(text, six.text_type) or isinstance(text, six.string_types)):
            return
        if not text:
            return
        else:
            return c.clean(text)

    return F.udf(clean_text, StringType())


# substitution
def create_udf_substitution(substitutions_dict):
    """
    create a substitution UDF

    :param substitutions_dict: substitution dictionary
    :return: Spark UDF to perform substitution on a Spark dataframe column
    """
    sflashtext = nlp4airbus_subst.Substitutions(substitution_dict=substitutions_dict)

    def subst_text(text):
        if text is None:
            return
        if not (isinstance(text, six.text_type) or isinstance(text, six.string_types)):
            return
        if not text:
            return
        else:
            return sflashtext.substitute(text)

    return F.udf(subst_text, StringType())


# stemmer
def create_udf_stemmer(language='english'):
    """
    create a stemmer UDF

    :param language: language of the text
    :return: Spark UDF to stem free text column
    """

    stemmer = nlp4airbus_stem.Stem(language=language)

    def stem_text(text):
        if text is None:
            return
        if not (isinstance(text, six.text_type) or isinstance(text, six.string_types)):
            return
        if not text:
            return
        else:
            return stemmer.tokenize_and_stem_long_text(text, output='string', remove_punctuations=True)
    return F.udf(stem_text, StringType())


# acronym expansion
def create_udf_acronym_expansion():
    """
    create a acronym expansion UDF

    :return: Spark UDF to perform acronym expansion on a Spark dataframe column
    """
    sflashtext = nlp4airbus_subst.Substitutions(substitution_dict='lexinet')

    def subst_text(text):
        if text is None:
            return
        if not (isinstance(text, six.text_type) or isinstance(text, six.string_types)):
            return
        if not text:
            return
        else:
            return sflashtext.substitute(text)

    return F.udf(subst_text, StringType())


# acronym expansion
def create_udf_ascii_normalization():
    """
    create an ASCII noramlization UDF

    :return: Spark UDF to noramlize a Spark dataframe free text column to ascii
    """
    def normalize_text(text):
        if text is None:
            return
        if not (isinstance(text, six.text_type) or isinstance(text, six.string_types)):
            return
        if not text:
            return
        else:
            return nlp4airbus_encoding.ascii_normalization(text)

    return F.udf(normalize_text, StringType())


# similarity
def create_udf_text_similarity(similarity_type='jaccard', normalize=True):
    """
    create aa text similarity UDF

    :param similarity_type: metric to compute similarity
    :param normalize: absolute or normalized similarity
    :return: Spark UDF to noramlize a Spark dataframe free text column to ascii
    """
    d = nlp4airbus_dist.Distance(similarity_type)

    def text_similarity(text1, text2):
        if (text1 is None) or (text2 is None):
            return
        if not (isinstance(text1, six.text_type) or isinstance(text1, six.string_types)):
            return
        if not (isinstance(text2, six.text_type) or isinstance(text2, six.string_types)):
            return
        if (not text1) or (not text2):
            return
        else:
            if normalize:
                return d.normalized_similarity(text1, text2)
            else:
                return d.similarity(text1, text2)

    return F.udf(text_similarity, StringType())
