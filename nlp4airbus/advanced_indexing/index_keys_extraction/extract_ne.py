"""
Created on 06/06/2018
@author: David ROUSSEL

Named entity recognition (NER) algorithms from nltk package implementation.
Many times NER doesn't tag consecutive NNPs as one NE. We reuse here a solution detailed in following post:
 https://stackoverflow.com/questions/24398536/named-entity-recognition-with-regular-expression-nltk

"""


from nltk import tokenize, pos_tag, ne_chunk
from nltk import Tree
from nlp4airbus.advanced_indexing.index_keys_extraction.linguistic_resources import StopNE


def get_continuous_chunks(text, chunk_func=ne_chunk, acronyms=StopNE):
    continuous_chunk = []
    current_chunk = []

    if len(text) > 2:
        # chunked can be improve by specific rules and tagger. see previous customization
        tokens = tokenize.word_tokenize(text)
        tags = pos_tag(tokens)
        chunked = chunk_func(tags)

        for subtree in chunked:
            if ((type(subtree) == Tree) and (" ".join([token.upper() for token, pos in subtree.leaves()]) in acronyms)):
                continue
            if ((type(subtree) == Tree) and (subtree.label() == 'PEOPLE') and (len(subtree.leaves()) > 1)):
                current_chunk.append(" ".join([token for token, pos in subtree.leaves()]))
            elif ((type(subtree) == Tree)):
                current_chunk.append(" ".join([token for token, pos in subtree.leaves()]))
            elif current_chunk:
                named_entity = " ".join(current_chunk)
                if named_entity not in continuous_chunk:
                    continuous_chunk.append(named_entity)
                current_chunk = []
            else:
                continue

    return continuous_chunk


def get_continuous_ne_chunks(text, acronyms=StopNE):
    continuous_chunk = []
    current_chunk = []

    if(len(text) > 2):
        # chunks can be improved by specific rules and taggers. See previous customization
        tokens = tokenize.word_tokenize(text)
        tags = pos_tag(tokens)
        chunked = ne_chunk(tags)
        for subtree in chunked:
            if ((type(subtree) == Tree) and (" ".join([token.upper() for token, pos in subtree.leaves()]) in acronyms)):
                continue
            if type(subtree) == Tree and subtree.label() == 'PEOPLE' and len(subtree.leaves()) > 1:
                current_chunk.append(" ".join([token for token, pos in subtree.leaves()]))
            elif type(subtree) == Tree:
                current_chunk.append(" ".join([token for token, pos in subtree.leaves()]))
            elif current_chunk:
                named_entity = " ".join(current_chunk)
                if named_entity not in continuous_chunk:
                    continuous_chunk.append(named_entity)
                current_chunk = []
            else:
                continue

    return continuous_chunk


def get_proper_names(text):
    tokens = tokenize.word_tokenize(text)
    pos = pos_tag(tokens)
    sentt = ne_chunk(pos, binary=False)
    person_list = []
    person = []
    name = ""
    for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
        for leaf in subtree.leaves():
            person.append(leaf[0])
        if len(person) > 1:  # avoid grabbing lone surnames
            for part in person:
                name += part + ' '
            if name[:-1] not in person_list:
                person_list.append(name[:-1])
            name = ''
        person = []

    return (person_list)
