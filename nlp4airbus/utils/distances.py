"""
Text distances, mainly a wrapper over `textdistance <https://github.com/orsinium/textdistance>`_ package.

.. note:: This module requires textdistance.
"""

try:
    import textdistance
except ImportError:
    pass
    # raise ImportError('Cannot import textdistance')


class JaccardDist:
    def similarity(self, text1, text2):
        a = set(text1.split())
        b = set(text2.split())
        c = a.intersection(b)
        return float(len(c)) / (len(a) + len(b) - len(c))

    def normalized_similarity(self, text1, text2):
        return self.similarity(text1, text2)


class Distance:
    """
    Wrapping class over ``textdistance`` package

    :param metric: Name of the metric
    :param qval: q-value for split sequences into q-grams. Possible values:

        * 1 (default) -- compare sequences by chars.
        * 2 or more -- transform sequences to q-grams.
        * None -- split sequences by words.
    :param as_Set: for token-based algorithms:

       * True -- t and ttt is equal.
       * False (default) -- t and ttt is different.
    """
    def __init__(self, metric, **kwargs):
        metric_lower = metric.lower()
        if metric_lower == 'hamming':
            self.dist = textdistance.Hamming(**kwargs)
        elif metric_lower == 'levenshtein':
            self.dist = textdistance.Levenshtein(**kwargs)
        elif metric_lower == 'damerau_levenshtein':
            self.dist = textdistance.DamerauLevenshtein(**kwargs)
        elif metric_lower == 'jaccard':
            self.dist = JaccardDist()
        elif metric_lower == 'cosine':
            self.dist = textdistance.Cosine(**kwargs)
        else:
            raise ValueError('Unknown metric')

    def distance(self, *seq):
        """
        compute distance between text sequences

        :param seq: sequence of strings
        :return: distance
        :rtype: int

        >>> from nlp4airbus.utils.distances import Distance
        >>> d = Distance('hamming')
        >>> d.distance("karolin", "kathrin")
        3
        """
        return self.dist.distance(*seq)

    def similarity(self, *seq):
        """
        compute similarity between text sequences

        :param seq: sequence of strings
        :return: similarity
        :rtype: int

        >>> from nlp4airbus.utils.distances import Distance
        >>> d = Distance('hamming')
        >>> d.similarity("karolin", "kathrin")
        4
        """
        return self.dist.similarity(*seq)

    def normalized_distance(self, *seq):
        """
        compute normalized distance between text sequences

        :param seq: sequence of strings
        :return: normalized distance (0 means equal, and 1 totally different)
        :rtype: float in [0;1]

        >>> from nlp4airbus.utils.distances import Distance
        >>> d = Distance('hamming')
        >>> d.normalized_distance("karolin", "kathrin")
        0.42857142857142855
        """
        return self.dist.normalized_distance(*seq)

    def normalized_similarity(self, *seq):
        """
        compute normalized similarity between text sequences

        :param seq: sequence of strings
        :return: normalized similarity (0 means totally different, and 1 equal)
        :rtype: float in [0;1]

        >>> from nlp4airbus.utils.distances import Distance
        >>> d = Distance('hamming')
        >>> d.normalized_similarity("karolin", "kathrin")
        0.5714285714285714
        """
        return self.dist.normalized_similarity(*seq)


if __name__ == '__main__':
    d = Distance('hamming')
    print(d.distance("karolin", "kathrin"))
    print(d.normalized_distance("karolin", "kathrin"))
    print(d.similarity("karolin", "kathrin"))
    print(d.normalized_similarity("karolin", "kathrin"))
