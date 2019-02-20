# -*- coding: utf-8 -*-
"""
Created on 06/06/2018
@author: Frederic SICOT and David ROUSSEL

This is a pythonic version of existing inflection algorithms, enrich with utils to deal with ngrams and original text
preservation constraints.
"""

import re


def singularize_last(ngrams_list):
    """
    Singularize last word of a list of ngrams. 
    It is linguistically motivated (inflected head of an engligh nous phrase is at the end. 
    Else it is complementation not well segmented during term extraction phase.
    By singularizing only the last part, simple exact matching is also still possible with the original text

    :param ngrams_list: string to singularize
    :return: list of ngrams where the last word of each is singularized
    """
    ngrams = [singularize(wrd) for wrd in ngrams_list]
    return ngrams


def singularize(word):
    """
    Singularizes English nouns

    :param word: string to singularize
    :return: singularized string

    >>> from nlp4airbus.lang.en.inflection import singularize
    >>> singularize("aircrafts")
    'aircraft'
    >>> singularize("stories")
    'story'
    """

    rules = [
        ['(?i)(quiz)zes$', '\\1'],
        ['(?i)(matr)ices$', '\\1ix'],
        ['(?i)(vert|ind)ices$', '\\1ex'],
        ['(?i)^(ox)en', '\\1'],
        ['(?i)(alias|status)es$', '\\1'],
        ['(?i)([octop|vir])i$', '\\1us'],
        ['(?i)(cris|ax|test)es$', '\\1is'],
        ['(?i)(shoe)s$', '\\1'],
        ['(?i)(o)es$', '\\1'],
        ['(?i)(bus)es$', '\\1'],
        ['(?i)([m|l])ice$', '\\1ouse'],
        ['(?i)(x|ch|ss|sh)es$', '\\1'],
        ['(?i)(m)ovies$', '\\1ovie'],
        ['(?i)(s)eries$', '\\1eries'],
        ['(?i)([^aeiouy]|qu)ies$', '\\1y'],
        ['(?i)([lr])ves$', '\\1f'],
        ['(?i)(tive)s$', '\\1'],
        ['(?i)(hive)s$', '\\1'],
        ['(?i)([^f])ves$', '\\1fe'],
        ['(?i)(^analy)ses$', '\\1sis'],
        ['(?i)((a)naly|(b)a|(d)iagno|(p)arenthe|(p)rogno|(s)ynop|(t)he)ses$',
            '\\1\\2sis'],
        ['(?i)([ti])a$', '\\1um'],
        ['(?i)(n)ews$', '\\1ews'],
        ['(?i)s$', ''],
    ]

    uncountable_words = set(['equipment', 'information', 'rice', 'money', 'species', 'series', 'fish', 'sheep', 'sms'] +
                            ["gallows", "proceedings", "breeches", "rabies", "britches", "headquarters", "herpes",
                             "scissors", "chassis", "high-jinks", "sea-bass", "clippers", "innings", "shears",
                             "contretemps", "jackanapes", "corps", "mackerel", "debris", "measles", "trout", "diabetes",
                             "mews", "tuna", "djinn", "mumps", "whiting", "eland", "news", "wildebeest", "elk",
                             "pincers", "sugar"] + ["apparatus", "impetus", "prospectus", "cantus", "nexus", "sinus",
                                                    "coitus", "plexus", "status", "hiatus"])

    irregular_words = {
        'people': 'person',
        'men': 'man',
        'children': 'child',
        'sexes': 'sex',
        'moves': 'move',
        "quizzes": "quiz",
        'feet': 'foot',
        'geese': 'goose',
        'teeth': 'tooth'
    }

    singular_s_es = ["acropolis", "chaos", "lens", "aegis",
                     "cosmos", "mantis", "alias", "dais", "marquis", "asbestos",
                     "digitalis", "metropolis", "atlas", "epidermis", "pathos",
                     "bathos", "ethos", "pelvis", "bias", "gas", "polis", "caddis",
                     "glottis", "rhinoceros", "cannabis", "glottis", "sassafras",
                     "canvas", "ibis", "trellis"]
    for word_l in singular_s_es:
        irregular_words[word_l + 'es'] = word_l

    sigular_ex_exes = ["apex", "latex", "vertex", "cortex", "pontifex", "vortex", "index", "simplex"]
    for word_l in sigular_ex_exes:
        irregular_words[word_l + 'es'] = word_l

    singular_on_a = ["criterion", "perihelion", "aphelion", "phenomenon", "prolegomenon", "noumenon",
                     "organon", "asyndeton", "hyperbaton"]
    for word_l in singular_on_a:
        irregular_words[word_l[:-2] + 'a'] = word_l

    lower_cased_word = word.lower()

    for uncountable_word in uncountable_words:
        if lower_cased_word[-1 * len(uncountable_word):] == uncountable_word:
            return word

    for irregular in irregular_words.keys():
        match = re.search('(' + irregular + ')$', word, re.IGNORECASE)
        if match:
            return re.sub('(?i)' + irregular + '$', match.expand('\\1')[0] + irregular_words[irregular][1:], word)

    for rule in range(len(rules)):
        match = re.search(rules[rule][0], word, re.IGNORECASE)
        if match:
            groups = match.groups()
            for k in range(0, len(groups)):
                if groups[k] is None:
                    rules[rule][1] = rules[
                        rule][1].replace('\\' + str(k + 1), '')

            return re.sub(rules[rule][0], rules[rule][1], word)

    return word


def add_singularize(word):
    """
    :param word: token to check
    :return: the singular form and keep original form between parenthesis
    """
    singular_form = singularize(word)
    if singular_form == word:
        return word
    else:
        return '%s (%s)' % (singular_form, word)


def does_it_starts(w, prefix_list):
    """
    check if token w does start with a given list of prefix.
    prefix is not necessary a linguistic prefix, it can be anything like
    ['utc:', 'source:', 'ph:', 'class:']

    :param w: token to check
    :param prefix_list:
    :return: True if beginning of word is in the prefix list
    """
    for prefix in prefix_list:
        if w.startswith(prefix):
            return True

    return False


if __name__ == '__main__':
    import doctest
    doctest.testmod()
