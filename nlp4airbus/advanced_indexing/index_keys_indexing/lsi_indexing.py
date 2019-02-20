"""
Created on 06/06/2018
@author: David ROUSSEL

high level functions from gensim LatentSemantic Indexing package.
"""

from gensim import corpora
from six import iteritems

def get_text_of(ids, dictionary):
    """Iterate over the collection, yielding one document at a time. A document
    is a sequence of words (strings) that can be fed into `Dictionary.doc2bow`.
    Each document will be fed through `preprocess_text`. That method should be
    overridden to provide different preprocessing steps. This method will need
    to be overridden if the metadata you'd like to yield differs from the line
    number.
    Returns:
        generator of lists of tokens (strings); each list corresponds to a preprocessed
        document from the corpus `input`.
    """
    words=[]
    try:
        for key, nb in ids:
             words.append(dictionary.id2token[key])
    except:
        pass
    return words



def clean_dictionary(stopwords, dictionary, min_freq=2):
    """remove stopwords or any antidico from the dictionary"""
	# remove stop words and words that appear only once
    stop_ids = [dictionary.token2id[stopword] for stopword in stopwords if stopword in dictionary.token2id()]
    happax = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq < min_freq]
	# remove stop words and words that appear only once
    dictionary.filter_tokens(bad_ids=stop_ids + happax)


def similar_to(bow_vec, lsi_vector, index,lsi, dfFilter,n=1,verbose=True,dfFilterField="mergedDescription"):
    '''display the n top most similar with highlighted keywords'''
    #bow_vec = dictionary.doc2bow(lsi_vector)
    my_vec_lsi = lsi[bow_vec] # convert the query to LSI space
    my_sims = index[my_vec_lsi] # perform a similarity query against the corpus
    # easy to extend to n similar docs
    my_sims = sorted(enumerate(my_sims), key=lambda item: -item[1])
    if verbose:
        print(str(len(my_sims))+" similar documents:\n")
        for i in range(n):
            my_text = dfFilter.loc[dfFilter.index[my_sims[i][0]],dfFilterField]
            for search_word in lsi_vector:
                #my_text = my_text.replace(search_word, '\033[44;33m{}\033[m'.format(search_word))
                my_text = my_text.replace(search_word.upper(), '\033[44;33m{}\033[m'.format(search_word.upper()))
            print("\nWith score ",str(my_sims[i][1]),":\n",my_text)
            
    return my_sims[:n]