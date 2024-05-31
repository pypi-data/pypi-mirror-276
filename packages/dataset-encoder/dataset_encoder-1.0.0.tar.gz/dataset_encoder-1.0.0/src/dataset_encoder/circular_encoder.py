from copy import deepcopy
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import pandas as pd


class CircularEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, limits=None, fit_replace=True, tol=1e-8):
        self.limits = limits
        self.fit_replace = fit_replace
        self.tol = tol
        self._shape = (0, 0)

    def __repr__(self):
        return "Circular Encoder"

    def __str__(self):
        return "Circular Encoder"

    def fit(self, X, y=None):

        # Shape setting
        self._shape = self.__set_shape(X)

        # Defining limit
        if self.fit_replace:
            self.limits = self.__set_limits(X)

        return self

    def transform(self, X, y=None):
        if self.limits is None:
            return deepcopy(X)

        # column_names only for DataFrame
        column_names = None

        # cast to numpy array
        if isinstance(X, pd.DataFrame):
            X_ndarray = X.to_numpy().reshape(self._shape)
            column_names = np.zeros(2 * X.columns.shape[0], dtype=object)
        else:
            X_ndarray = X.reshape(self._shape)

        # main encoding
        result_sin = np.sin((2 * np.pi * X_ndarray) / self.limits)
        result_cos = np.cos((2 * np.pi * X_ndarray) / self.limits)

        result_sin[np.abs(result_sin) < self.tol] = 0.0
        result_cos[np.abs(result_cos) < self.tol] = 0.0

        # combine encoded arrays
        result = np.zeros((self._shape[0], self._shape[1] * 2))
        result[:, np.arange(0, result.shape[1], 2)] = result_sin
        result[:, np.arange(1, result.shape[1], 2)] = result_cos

        # set column_names names and return result
        if column_names is not None:
            column_names[np.arange(0, result.shape[1], 2)] = np.array([f'sin_{col}' for col in X.columns])
            column_names[np.arange(1, result.shape[1], 2)] = np.array([f'cos_{col}' for col in X.columns])
            return pd.DataFrame(result, columns=column_names).infer_objects()
        else:
            return result

    @staticmethod
    def __set_shape(X):
        if len(X.shape) == 1:
            return (X.shape[0], 1)
        elif len(X.shape) > 2:
            raise ValueError(f"You need 2 dimensions instead of {len(X.shape)}")
        else:
            return X.shape

    @staticmethod
    def __set_limits(X):
        if isinstance(X, pd.DataFrame):
            return np.max(np.abs(X.to_numpy()), axis=0) + 1
        else:
            return np.max(np.abs(X), axis=0) + 1
