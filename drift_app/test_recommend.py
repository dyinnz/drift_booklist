import numpy as np
from recommender import FM_Recommender
import sys

if __name__ == '__main__':

    n_user, n_book = int(sys.argv[1]), int(sys.argv[2])
    fm_recommender = FM_Recommender(20, float(sys.argv[3]))
    X = np.random.random((n_user, n_book))
    for i in range(n_user):
        for j in np.random.choice(list(range(n_book)), int(0.66 * n_book), replace=None):
            X[i, j] = 0

    X[abs(X) > 1.0] = 1.0 / abs(X[abs(X) > 1.0])

