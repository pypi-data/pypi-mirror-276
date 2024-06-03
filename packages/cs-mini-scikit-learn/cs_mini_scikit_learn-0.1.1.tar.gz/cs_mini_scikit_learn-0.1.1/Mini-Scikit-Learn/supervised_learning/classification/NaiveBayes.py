import numpy as np
from supervised_learning.BaseEstimator import BaseEstimator


class NaiveBayes(BaseEstimator):
    """
    Naive Bayes classifier.

    Methods
    -------
    fit(X, y)
        Fit the Naive Bayes classifier to the training data.
    
    predict(X)
        Predict class labels for samples in X.
    """

    def fit(self, X, y):
        """
        Fit the Naive Bayes classifier to the training data.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The training input samples.
        
        y : array-like of shape (n_samples,)
            The target values (class labels).
        """
        if not isinstance(X, np.ndarray) or not isinstance(y, np.ndarray):
            raise TypeError("X and y must be numpy arrays.")
        if X.shape[0] != y.shape[0]:
            raise ValueError("The number of samples in X and y must be equal.")

        n_samples, n_features = X.shape
        self.classes_ = np.unique(y)
        n_classes = len(self.classes_)

        self.mean_ = np.zeros((n_classes, n_features), dtype=np.float64)
        self.var_ = np.zeros((n_classes, n_features), dtype=np.float64)
        self.priors_ = np.zeros(n_classes, dtype=np.float64)

        for idx, class_ in enumerate(self.classes_):
            X_class = X[y == class_]
            self.mean_[idx, :] = X_class.mean(axis=0)
            self.var_[idx, :] = X_class.var(axis=0)
            self.priors_[idx] = X_class.shape[0] / float(n_samples)

    def predict(self, X):
        """
        Predict class labels for samples in X.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The input samples.

        Returns
        -------
        y_pred : array-like of shape (n_samples,)
            The predicted class labels.
        """
        if not isinstance(X, np.ndarray):
            raise TypeError("X must be a numpy array.")
        
        return np.array([self._predict(x) for x in X])

    def _predict(self, x):
        posteriors = []
        for idx, class_ in enumerate(self.classes_):
            prior = np.log(self.priors_[idx])
            posterior = np.sum(np.log(self._pdf(idx, x)))
            posterior = prior + posterior
            posteriors.append(posterior)
        return self.classes_[np.argmax(posteriors)]

    def _pdf(self, class_idx, x):
        mean = self.mean_[class_idx]
        var = self.var_[class_idx]
        if np.any(var == 0):
            raise RuntimeError("One or more features have zero variance.")
        numerator = np.exp(-((x - mean) ** 2) / (2 * var))
        denominator = np.sqrt(2 * np.pi * var)
        return numerator / denominator
