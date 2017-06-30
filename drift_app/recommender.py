import numpy as np


class FM_Recommender():
    """
    Recommender based on Factorize Matrix method.
    """

    def __init__(self, n_components, eta=0.01, alpha=0.01, beta=0.01, max_iter=-1, epsilon=0.1):
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
        self.U = np.random.random((n_user, self.n_components)) / np.sqrt(self.n_components)
        self.M = np.random.random((n_book, self.n_components)) / np.sqrt(self.n_components)
        self.bu = np.random.random((n_user))
        self.bm = np.random.random((n_book))
        self.overall_mean = 0.1 * np.random.random()
        return self

    def updata_shape(self, n_user, n_book):
        old_n_user = self.U.shape[0]
        old_n_book = self.M.shape[0]
        if old_n_user < n_user:
            self.U = np.row_stack((self.U, np.random.random(self.n_components)))
        else:
            self.U = self.U[np.random.choice(range(old_n_user), n_user, replace=False), :]
        if old_n_book < n_book:
            self.M = np.row_stack((self.M, np.random.random(self.n_components)))
        else:
            self.M = self.M[np.random.choice(range(old_n_book), n_book, replace=False), :]

    def fit(self, X):
        """
        train model on data X.
        :param X: np.ndarray, shape:(n_user, n_book), user-book rating matrix, whose value from 0 to 1
        :return: self
        """
        self.n_user, self.n_book = X.shape
        if not hasattr(self, 'U') or not hasattr(self, 'M') or not hasattr(self, 'bu') or \
                not hasattr(self, 'bm') or not hasattr(self, 'overall_mean'):
            self.init_param(self.n_user, self.n_book)
        elif self.U.shape[0] != X.shape[0] or self.M.shape[0] != X.shape[1]:
            self.updata_shape(self.n_user, self.n_book)
        mask = (X != 0)

        it = 0
        is_converg = False
        while not is_converg:
            if self.max_iter > 0 and it > self.max_iter:
                break
            delta_E = X - self.U.dot(self.M.T) - self.bu.reshape(-1, 1) - self.overall_mean - self.bm
            delta_U = (mask * delta_E).dot(self.M) - self.alpha * self.U
            delta_M = (mask * delta_E).T.dot(self.U) - self.beta * self.M
            delta_bu = np.sum(mask * delta_E, axis=1) - self.alpha * self.bu
            delta_bm = np.sum(mask * delta_E, axis=0) - self.beta * self.bm
            if it % 1000 == 0:
                print('Iter %d:' % it, np.sum(mask * delta_E))
            if abs(np.sum(mask * delta_E)) > 10000:
                print('Iter %d:boom!' % it, np.sum(mask * delta_E))
                break

            self.U = self.U + self.eta * delta_U
            self.M = self.M + self.eta * delta_M
            self.bu = self.bu + self.eta * delta_bu
            self.bm = self.bm + self.eta * delta_bm

            it += 1
            is_converg = abs(np.sum(mask * delta_E)) < self.epsilon
            if is_converg:
                print('Iter %d:Converge! DeltaE: %f' % (it, np.sum(mask * delta_E)))

        # self.V = self.U.dot(self.M.T) + self.bu.reshape(-1, 1) + self.overall_mean + self.bm
        self.V = (self.U.dot(self.M.T) + self.bu.reshape(-1, 1) + self.overall_mean + self.bm) * np.bitwise_not(mask) + X
        return self

    def topK(self, id_user, k, exclude=None):
        if not hasattr(self, 'V'):
            print("The model hasn't been trained yet.")
            return
        rating = self.V
        if exclude is not None:
            rating = np.delete(rating, exclude, axis=1)
        return self.V[id_user].argsort()[:-(k + 1):-1]


class Tag_Based_Recommender():
    """
    Recommender based on tag system.
    Useful for cool boot, assume user has selected several tags he's interested in,
    then tag based recommender can recommend some books fit the tags.
    """
    def __init__(self, book_tags):
        """
        initialize the recommender.
        :param book_tags: book_tags matrix M, M[i, j] = 1 if book i has tag j, otherwise 0.
        """
        self.book_tags = book_tags

    def topK_books(self, user_tags, k, exclude=None):
        """
        get top K books for user.
        :param user_tags: user_tag vector v, v[j] = 1 if user is interested in tag j, otherwise 0.
        :param k: number of books.
        :return: K-size list containing k book id.
        """
        book_tags = self.book_tags
        if exclude is not None:
            book_tags = np.delete(book_tags, exclude, axis=0)
        return self.book_tags.dot(user_tags).argsort()[:-(k + 1):-1]


    def topK_booklists(self, booklist_book, k):
        return None


class Item_CF_Recommender():
    def __init__(self):
        pass

    def fit(self, X):
        pass
