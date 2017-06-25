import numpy as np


class FM_Recommender():
    """
    Recommender based on Factorize Matrix method.
    """
    def __init__(self, n_components, eta=0.01, alpha=0.01, beta=0.01, max_iter=-1, epsilon=1.0):
        """
        init the model.
        :param n_components: components(latent factor) count.
        :param eta: learing rate.
        :param alpha: normalization parameter 1.
        :param beta: normalization parameter 2.
        :param max_iter: max training iteration.
        :param epsilon: parameter to measure whether the model is converged.
        """
        self.n_components = n_components
        self.eta = eta
        self.alpha = alpha
        self.beta = beta
        self.max_iter = max_iter
        self.epsilon = epsilon

    def init_param(self, n_user, n_book):
        """
        Init parameters, U(user-factor matrix), M(book-factor matrix), bu(user rate vector), bm(book rate vector),
        overall_mean(overall rate).
        :param n_user: user number.
        :param n_book: book number.
        :return: self
        """
        self.U = np.random.normal(0, 1, (n_user, self.n_components))
        self.M = np.random.normal(0, 1, (n_book, self.n_components))
        self.bu = np.random.normal(0, 1, (n_user))
        self.bm = np.random.normal(0, 1, (n_book))
        self.overall_mean = np.random.normal(0, 1)
        return self

    def fit(self, X, y=None):
        self.n_user, self.n_book = X.shape
        if not hasattr(self, 'U') or not hasattr(self, 'M') or not hasattr(self, 'bu') or \
                not hasattr(self, 'bm') or not hasattr(self, 'overall_mean'):
            self.init_param(self.n_user, self.n_book)
        elif self.U.shape[0] != X.shape[0] or self.M.shape[0] != X.shape[1]:
            self.init_param(self.n_user, self.n_book)
        mask = (X != 0)

        it = 0
        is_converg = False
        while not is_converg and (self.max_iter > 0 and it < self.max_iter):
            delta_E = X - self.U.dot(self.M.T) - self.bu - self.bm - self.overall_mean
            delta_U = (mask * delta_E).dot(self.M) - self.alpha * self.U
            delta_M = (mask * delta_E).T.dot(self.U)
            delta_bu = np.sum(mask * delta_E, axis=1) - self.alpha * self.bu
            delta_bm = np.sum(mask * delta_E, axis=0) - self.beta * self.bm

            self.U = self.U - self.eta * delta_U
            self.M = self.M - self.eta * delta_M
            self.bu = self.bu - self.eta * delta_bu
            self.bm = self.bm - self.eta * delta_bm

            it += 1
            is_converg = delta_E < self.epsilon

        self.V = self.U.dot(self.M.T)
        return self


    def topK(self, id_user, k):
        if not hasattr(self, 'V'):
            print("The model hasn't been trained yet.")
            return
        return self.V[id_user].argmax()[:-(k+1):-1]


class Content_Based_Recommender():
    def __index__(self, book_tags):
        self.book_tags = book_tags

    def predict(self, user_tags, k):
        return self.book_tags.dot(user_tags).argsort()[:-(k+1):-1]
