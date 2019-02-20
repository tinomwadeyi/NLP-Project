"""
Created on 06/06/2018
@author: David ROUSSEL

Noun phrase recognition algorithms from nltk package implementation.
Many times, the tags from which the algorithms rely are wrong on technical english text, so assessment of performances 
is necessary before effective use of NP extraction.

"""
import itertools
from nltk import word_tokenize, pos_tag
import nltk


def get_phrases(chunks):
    flat_list = list(itertools.chain.from_iterable(chunks))
    flat_list = [tree for tree in flat_list if type(tree) == nltk.tree.Tree]
    flat_list.sort()


def get_NP(chunks):
    """Finds NP (nounphrase) leaf nodes of a chunk tree."""

    return [subtree for subtree in chunks.subtrees(filter=lambda t: t.label() == 'NP')]


NP = "NP: {(((<V\w+>|<JJ>|<NN\w?>).*<NN\w?>)|(.*<NN\w?>(.*<CD>)))}"
chunkr = nltk.RegexpParser(NP) 


def get_all_NP(text, tagger=pos_tag, chunker=chunkr):
    '''
    :param tagger: regexp_tagger with various backoff or a simpler one (by default nltk pos_tag)
    :param chunker: chunker previously initialize with init_tagger_for_np_extract.init_np_regexpchunker() method
    :return: list of ngrams where the last word of each is singularized
    '''
    if(len(text) > 2):
        # chunked = chunk_func(pos_tag(word_tokenize(text)))
        tag_list = tagger.tag(word_tokenize(text))
        phrases = chunker.parse(tag_list)
        leaves = [subtree.leaves() for subtree in phrases.subtrees(filter=lambda t: t.label() == 'NP')]
        return [' '.join([w for (w, t) in l]) for l in leaves]


def init_np_chunker():
        """ Method that defines an XBar grammar to extract NP """

        NP = r"""NBAR:
                    {(<VB\w?>|<NN\w?>|<JJ>)+<NN\w?>}   # words recognized as tensed V, Nouns and Adjectives, terminated with Nouns
                NP:
                    {<NBAR><AT|OF|TO><NBAR>}      # prep included
                    {<NBAR><CD><NCC><NBAR>}
                    {<NBAR><CD><NCC><CD>}
                    {<NBAR><CD>}
                    {<NN><CD>}
                    {<NBAR>}
        """

        chunker = nltk.RegexpParser(NP)

        return chunker


