"""
Some text encoding functions
"""
try:
    import unicodedata2
except ImportError:
    pass


def ascii_normalization(text):
    """
    Normalize text to ascii

    :param text: text to normalize
    :return: ASCII-normalized text

    :warnings: Only works on Python 2

    """
    return unicodedata2.normalize('NFKD', unicode(text)).encode('ascii', 'ignore')
