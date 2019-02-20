"""
Created on 06/06/2018
@author: David ROUSSEL

functions to initialize tagger (and associated chunckers) used by extract_np
"""
import nltk
import nltk.tag
from nltk.tag.perceptron import PerceptronTagger
from nltk import pos_tag

def init_max_ent_tagger():

    # take care nltk-data is available in the codeworkbook environment or in python transform

    #    """
    #    >>> evaluate_tags(init_max_ent_tagger(),[('RESET', 'VBP'), ('THE', 'DT'), ('ULTRAMAIN','NN'), ('SYSTEMS', 'NNS')])
    #    0.25
    #    """

    path = "nltk:taggers/maxent_treebank_pos_tagger/english.pickle"
    t1 = nltk.data.load(path)
    return t1


class myNgramTagger(nltk.NgramTagger):
    """
    My override of the NLTK NgramTagger class that considers previous
    tokens rather than previous tags for context.
    """

    def __init__(self, n, train=None, model=None,
                 backoff=None, cutoff=0, verbose=False):
        if model is None: 
            self.word_contexts = {
            (('as',), 'per') : "LOC",  # per = prep loc
            (('to',), 'be') : "LOC",
            (('1',),  'and') : "NCC",
            (('2',), 'and') : "NCC",
            (('3',), 'and') : "NCC",
            (('1',),  'or') : "NCC",
            }
        else:
            self.word_contexts = model
        nltk.NgramTagger.__init__(self, n, train, self.word_contexts, backoff, cutoff, verbose)

    def context(self, tokens, index, history):
        # tag_context = tuple(history[max(0,index-self._n+1):index])
        tag_context = tuple(tokens[max(0, index - self._n + 1): index])
        return tag_context, tokens[index]

    def set_word_context(self, wc):
        self.word_contexts = wc


def init_ngram_tagger():
    ngram_tagger = myNgramTagger(2, model=None, backoff=init_max_ent_tagger())
    return ngram_tagger

# alternatively here is a simpler code to iniatilize a simpler unigram tagger
# enrich with all not well recognized functional word (at least in capital letters)
#predefinedModel= {'TO':'TO','IF':'IN'}
#t2=nltk.tag.UnigramTagger(model=predefinedModel, backoff=backofftagger())
#t2=nltk.tag.UnigramTagger(model=predefinedModel, backoff=t1)

# default perceptron tagger redefined by the previous class
# tag_list = [nltk.pos_tag(w) for w in tokens]
# tag_list = [t2.tag(w) for w in tokens]

#chunks = [chunkr.parse(sublist) for sublist in tag_list]


#regexp_tagger = nltk.RegexpTagger(patterns,backoff=pos_tag)
def init_np_regexpchunker():

    patterns = [
        (r'(?i)(BE|IS|ARE|WAS)$', 'VAUX'), 
        (r'(?i)(NOT|DOESNT|ISNT)$', 'RB'),   # negation
        (r'(?i).*ED$', 'VBD'),                # simple past
        (r'(?i).*MENT$', 'NDV'),                # deverbal noun 
        (r'(?i).*OULD$', 'MD'),               # modals
        (r'(?i)(CAN|COULD|MUST|SHOULD)$', 'MD'),        # modals
        (r'(?i).*\'S$', 'NN$'),               # possessive nouns
        (r'(?i)^-?[0-9]+(.[0-9]+)?$', 'CD'),  # cardinal numbers
        (r'(?i)(THE|A|AN|NO|NIL)$', 'DT'),   # articles 
        (r'(?i).*ABLE$', 'JJ'),                # adjectives 
        (r'(?i).*NESS$', 'NN'),                # nouns formed from adjectives
        (r'(?i).*LY$', 'RB'),                  # adverbs
        (r'(?i)AT$', 'AT'),                  # special interpretation required
        (r'(?i)TO$', 'TO'),                  # special interpretation required
        (r'(?i)OF$', 'OF'),                  # special interpretation required
        (r'(?i)(LIKE|AS|THAN)$', 'COMP'),         # special interpretation required
        (r'(?i)(HE|SHE|IT|I|ME|YOU)$', 'PRP'), # pronouns
        (r'(?i)(HIS|HER|ITS)$', 'PRP$'),    # possesive
        (r'(?i)(OUR|MY|YOUR|YOURS)$', 'PRP$'),   # possesive
        (r'(?i)(ON|IN|IF)$', 'IN'),# time prepopsitions
        (r'(?i)(FOR|AGO|BEFORE)$', 'IN'),# time prepopsitions
        (r'(?i)(BOTH|BUT|EITHER|LESS|MINUS|NOR|PLUS|SO)$', 'CC'),# logic coord
        (r'(?i)(AMONG|UPON|OUT|INSIDE|DESPITE|LIKE)$', 'IN'),# logic prepositions
        (r'(?i)(TILL|UNTIL|SINCE)$', 'IN'),        # time prepopsitions
        (r'(?i)(BY|BESIDE)$', 'IN'),          # space prepopsitions
        (r'(?i)(UNDER|BELOW|)$', 'IN'),      # space prepopsitions
        (r'(?i)(OVER|ABOVE)$', 'IN'),        # space prepopsitions
        (r'(?i)(ACROSS|THROUGH)$', 'IN'),# space prepopsitions
        (r'(?i)(INTO|TOWARDS)$', 'IN'),    # space prepopsitions
        (r'(?i)(ONTO|FROM)$', 'IN'),          # space prepopsitions 
        (r'\.$','.'), (r'\,$',','), (r'\?$','?'),    # fullstop, comma, Qmark
        (r'\($','('), (r'\)$',')'),             # round brackets
        (r'\[$','('), (r'\]$',')'),             # square brackets
        (r'(-|:|;)$', ':')
        # WARNING : Put the default value in the end IF NO BACKOFF
    #    (r'.*', 'NN')                      # nouns (default)
        ]

    regexp_tagger = nltk.RegexpTagger(patterns, backoff=init_ngram_tagger())
    return regexp_tagger


def evaluate_tags(tagger, test_sents):
    '''to evaluate the tagger eprformance against a reference'''
    return tagger.evaluate(test_sents)

# generate a test through doc test


if __name__ == '__main__':

    test_sents = [
 [('RESET', 'VBP'), ('THE', 'DT'), ('ULTRAMAIN','NN'), ('SYSTEMS', 'NNS')],
 [('USE', 'VBP'), ('THE', 'DT'), ('RESET', 'JJ'), ('FUNCTION', 'NN'), ('AS', 'COMP'), ('PER', 'LOC'), ('REF', 'NN')],
 [('REPORT', 'VBP'), ('HAND', 'NN'), ('LANDING', 'NN'), ('.', '.'), ('NO', 'DT'), ('HARD', 'JJ'), ('LANDING', 'NN')],
 [('PLS', 'NNS'), ('REVALIDATE', 'VBP'), ('DAILY', 'RB'), ('IF', 'IN'), ('REQUIRED', 'VBD'), ('BEFORE', 'IN'), ('DEPARTURE', 'NN')],
 [('CLOSED', 'VBD'), ('DOOR', 'NN'), ('WRNG', 'NN')],
 [('HARD', 'JJ'), ('LANDING', 'NN'), ('REPORT', 'NN'), ('GENERATED', 'VBD'), ('.', '.'), ('CREW', 'NN'),
 ('ASSESSMENT', 'NDV'), ('NO', 'DT'), ('HARD', 'JJ'), ('LDG', 'NN')],
 [('NOTICE', 'NN'), ('TO', 'TO'), ('CREW', 'NN'), ('RAISED', 'VBD'), ('START', 'VB'), ('ENGINE', 'NN'),
 ('1', 'CD'), ('AND', 'NCC'), ('ENGINE', 'NN'), ('2', 'CD'), ('INDIVIDUALLY', 'RB'), ('TO', 'TO'), ('REDUCE', 'VB'),
 ('APU', 'NNP'), ('MARGINS', 'NNS')]
]
    print( "Taggers initialization tests")
    #print(evaluate_tags(init_max_ent_tagger(),test_sents))
    #print(evaluate_tags(init_max_ent_tagger(),[[('RESET', 'VBP'), ('THE', 'DT'), ('ULTRAMAIN','NN'), ('SYSTEMS', 'NNS')]]))
    print(evaluate_tags(init_np_regexpchunker(), test_sents))
    print(evaluate_tags(init_np_regexpchunker(), [[('RESET', 'VBP'), ('THE', 'DT'), ('ULTRAMAIN','NN'), ('SYSTEMS', 'NNS')]]))