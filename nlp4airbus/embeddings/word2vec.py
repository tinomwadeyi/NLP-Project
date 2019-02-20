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


class Word2Vec:
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
        self.loss = []

    def fit(self, documents, **kwargs):
        """
        Train the word2Vec embeddings. Can be called several times

        :param documents: list of lists of tokens, or list of documents (in that case, each document will be
           automatically tokenized with ``gensim.utils.simple_preprocess()``
        :param kwargs: additional parameetrs to gensim Word2Vec model
        """
        # tokenize if needed
        if isinstance(documents[0], six.text_type) or isinstance(documents[0], six.string_types):
            documents = [gensim.utils.simple_preprocess(t) for t in documents]

        # create model
        self.model = gensim.models.Word2Vec(documents, size=self.size, window=self.window, min_count=self.min_count,
                                            alpha=self.alpha, min_alpha=self.alpha, **kwargs)

        # training loops
        alpha = self.alpha
        for k in range(self.passes):
            self.model.alpha, self.model.min_alpha = alpha, alpha
            self.model.train(documents, total_examples=len(documents), epochs=1, compute_loss=True)
            self.loss.append(self.model.get_latest_training_loss())

            if self.shuffle_doc:
                random.shuffle(documents)

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
            self.model = gensim.models.Word2Vec.load(file_obj)
        else:
            self.model = gensim.models.Word2Vec()
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

    wv = Word2Vec(passes=200)
    wv.fit(tlb['free_text'].tolist())
    # print(wv.get_vector('galley'))
    print(wv.most_similar('galley', 10))
