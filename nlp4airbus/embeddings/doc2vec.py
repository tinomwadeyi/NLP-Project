"""
Train Word2Vec embeddings.

.. note:: This module requires Gensim
"""
import random
import six

try:
    import gensim
except ImportError:
    pass


class Doc2Vec:
    """
    Doc2Vec model

    :ivar model: Gensim W
    :ivar var2: initial value: par2
    """
    def __init__(self, window_size=5, size=100, min_count=3, shuffle_doc=True,
                 alpha=0.025, min_alpha=0.0001, passes=100):
        """

        :param window_size: Maximum distance between the current and predicted word within a sentence
        :type window_size: int
        :param size:  Dimensionality of the word vectors
        :type size: int
        :param min_count: Ignores all words with total frequency lower than this
        :type min_count: int
        :param shuffle_doc: shuffle documents durint training iterations
        :type shuffle_doc: bool
        :param alpha: initial learning rate
        :type alpha: float
        :param min_alpha: Learning rate will linearly drop to **min_alpha** as training progresses
        :type min_alpha: float
        :param passes: number of learning iterations
        :type passes: int
        """
        self.alpha = alpha
        self.min_alpha = min_alpha
        self.passes = passes
        self.window = window_size
        self.size = size
        self.min_count = min_count
        self.shuffle_doc = shuffle_doc

        self.alpha_delta = (self.alpha - self.min_alpha) / self.passes
        self.model = None

    @staticmethod
    def _tag_doc(documents):
        """
        clean, tokenize document and tag them for Doc2Vec

        :param documents: list of documents
        :return: list of tagged tokens
        """
        if isinstance(documents[0], six.text_type) or isinstance(documents[0], six.string_types):
            for i, line in enumerate(documents):
                yield gensim.models.doc2vec.TaggedDocument(gensim.utils.simple_preprocess(line), ['idx_' + str(i)])
        else:
            for i, line in enumerate(documents):
                yield gensim.models.doc2vec.TaggedDocument(line, ['idx_' + str(i)])

    def fit(self, documents, **kwargs):
        """
        Train the word2Vec embeddings. Can be called several times

        :param documents: list of lists of tokens, or list of documents (in that case, each document will be
           automatically tokenized with ``gensim.utils.simple_preprocess()``
        :param kwargs: additional parameetrs to gensim Word2Vec model
        """
        # tokenize if needed
        tag_docs = list(self._tag_doc(documents))

        # create model
        self.model = gensim.models.doc2vec.Doc2Vec(vector_size=self.size, min_count=self.min_count, workers=3,
                                                   alpha=self.alpha, dm=1, min_alpha=self.min_alpha)
        self.model.build_vocab(tag_docs)

        # training loops
        alpha = self.alpha
        for k in range(self.passes):
            self.model.alpha, self.model.min_alpha = alpha, alpha
            self.model.train(tag_docs, total_examples=len(documents), epochs=1)

            if self.shuffle_doc:
                random.shuffle(tag_docs)

            # decrease the learning rate
            alpha -= self.alpha_delta
            alpha = max(alpha, self.min_alpha)

    def save_model(self, file_obj, full_model=True):
        """
        save Word2Vec model

        :param file_obj: file to save the model to
        :param full_model: save full model (needed to perform another train session) (see
           `Gensim doc <https://radimrehurek.com/gensim/models/keyedvectors.html#why-use-keyedvectors-instead-of-a-full-model>`_)
        """
        if full_model:
            self.model.save(file_obj)
        else:
            self.model.wv.save_word2vec_format(file_obj)

    def load_model(self, file_obj, full_model=True):
        """
        load word2vec model

        :param file_obj: file to load model from
        :param full_model: save full model (needed to perform another train session)
           (see `Gensim doc <https://radimrehurek.com/gensim/models/keyedvectors.html#why-use-keyedvectors-instead-of-a-full-model>`_)
        :return: Gensim Word2Vec model or KeyedVectors
        """
        if full_model:
            self.model = gensim.models.Doc2Vec.load(file_obj)
        else:
            self.model = gensim.models.Doc2Vec()
            self.model.wv = gensim.models.KeyedVectors.load(file_obj)

    def most_similar(self, word, topn):
        """
        Find most similar term

        :param word: token to find similarity
        :param topn: number of similar token
        :return:
        """
        return self.model.wv.most_similar(word, topn=topn)

    def get_vector(self, token):
        """
        get embeddings of a token

        :param token: token
        :return: list of floats
        """
        return self.model[token]


if __name__ == '__main__':
    import pandas as pd

    tlb = pd.read_csv('/Users/sicot/projets/NLP/embeddings/only_text_lr.csv', nrows=30000).fillna('')
    tlb['free_text'] = tlb['snag_job_description'].str.cat(tlb['snag_cor_action'], sep=' ').str.lower()
    doc_list = tlb['free_text'].tolist()

    wv = Doc2Vec(passes=10)
    wv.fit(doc_list)

    doc_id = random.randint(0, len(tlb) - 1)
    inferred_vector = wv.model.infer_vector(doc_list[doc_id])
    sims = wv.docvecs.most_similar([inferred_vector], topn=len(wv.docvecs))
    # print('Document: «{}»\n'.format(tlb.loc['free_text', 0])))
    # print(u'SIMILAR/DISSIMILAR DOCS PER MODEL %s:\n' % wv.model)
    # for label, index in [('MOST', 0), ('SECOND-MOST', 1), ('MEDIAN', len(sims) // 2), ('LEAST', len(sims) - 1)]:
    #     print(u'%s %s: «%s»\n' % (label, sims[index], ' '.join(train_corpus[sims[index][0]].words)))
