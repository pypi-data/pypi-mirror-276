import numpy as np

class SupportVectorMachine:

    def __init__(self, learning_rate=0.001, lambda_param=0.01, n_iters=1000):
        """Initialize the Support Vector Machine."""
        self.lr = learning_rate
        self.lambda_param = lambda_param
        self.n_iters = n_iters
        self.w = None
        self.b = None

    def fit(self, X, y):
        """
        Fit the SVM model to the training data.

        Parameters:
        -----------
        X : numpy.ndarray
            Training data.
        y : numpy.ndarray
            Target labels.
        """
        n_samples, n_features = X.shape

        y_ = np.where(y <= 0, -1, 1)

        self.w = np.zeros(n_features)
        self.b = 0

        for _ in range(self.n_iters):
            for idx, x_i in enumerate(X):
                condition = y_[idx] * (np.dot(x_i, self.w) - self.b) >= 1
                if condition:
                    self.w -= self.lr * (2 * self.lambda_param * self.w)
                else:
                    self.w -= self.lr * (2 * self.lambda_param * self.w - np.dot(x_i, y_[idx]))
                    self.b -= self.lr * y_[idx]

    def predict(self, X):
        """
        Predict class labels for samples in X.
        Parameters:
        -----------
        X : numpy.ndarray
            Test data.

        Returns:
        --------
        numpy.ndarray
            Predicted class labels.
        """
        approx = np.dot(X, self.w) - self.b
        return np.sign(approx)
