from copy import deepcopy
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import pandas as pd
import sklearn.preprocessing as skpr


class NumericalEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, cols=None, fit_replace=True, encoder='standard', numeric_rate=0.1,
                 rated_search=True, only_float=True, **encoder_params):

        self._encoders_list = {'standard': skpr.StandardScaler,
                               'min_max': skpr.MinMaxScaler, 
                               'robust': skpr.RobustScaler,
                               'normalizer': skpr.Normalizer,
                               'max_abs': skpr.MaxAbsScaler}

        self.only_float = only_float
        self.cols = np.array(cols) if cols is not None else None
        self.fit_replace = fit_replace
        self.encoder_name = encoder
        self.numeric_rate = numeric_rate
        self.rated_search = rated_search
        self.encoder_params = encoder_params
        self._encoder = None

    def __repr__(self):
        return "NumericalEncoder"

    def __str__(self):
        return "NumericalEncoder"

    def fit(self, X, y=None, **fit_params):
        # defining numerical columns
        if self.cols is None or self.fit_replace:
            self.cols = self.define_cols(X)

        try:
            if not self.cols.shape[0]:
                return self
        except IndexError:
            raise IndexError("cols should be a numpy array")

        # save self.cols and get indices for X
        saved_cols = self.cols.copy()
        self.cols = self.cols_to_numeric(X)

        if not self.cols.shape[0]:
            self.cols = saved_cols
            return self

        # defining the encoder
        self._encoder = self._encoders_list[self.encoder_name](**self.encoder_params)

        # fitting the encoder
        X_ndarray = X.to_numpy()[:, self.cols] if isinstance(X, pd.DataFrame) else X[:, self.cols]
        self._encoder.fit(X_ndarray, y, **fit_params)

        # self.cols backup
        self.cols = saved_cols

        return self

    def transform(self, X, y=None):
        try:
            if self.cols is None or not self.cols.shape[0] or self._encoder is None:
                return deepcopy(X)
        except IndexError:
            raise IndexError("cols should be a numpy array")

        # save self.cols and get indices for X
        saved_cols = self.cols.copy()
        self.cols = self.cols_to_numeric(X)

        if not self.cols.shape[0]:
            self.cols = saved_cols
            return deepcopy(X)

        column_names = None

        # cast to numpy array
        if isinstance(X, pd.DataFrame):
            X_ndarray = X.iloc[:, self.cols].to_numpy().astype(float)
            column_names = X.columns.to_numpy(dtype=object).copy()
        else:
            X_ndarray = X[:, self.cols].astype(float)

        # getting the resulting column names
        if column_names is not None:
            column_names[self.cols] = np.array([f'{self.encoder_name}_{name}' for name in column_names[self.cols]])

        # only numerical columns here
        result = self._encoder.transform(X_ndarray)

        if isinstance(X, pd.DataFrame):
            # saving X dtypes
            not_cols = list(set(np.arange(X.shape[1])) - set(self.cols))
            saved_dtypes = X.dtypes.to_dict()
            unmodified_dtypes = dict([(X.columns[col], saved_dtypes[X.columns[col]]) for col in not_cols])

            X_ndarray = deepcopy(X.to_numpy(dtype=object))
            X_ndarray[:, self.cols] = result
            result = pd.DataFrame(X_ndarray, columns=column_names).astype(dtype=unmodified_dtypes).infer_objects()
        else:
            X_ndarray = deepcopy(X)
            X_ndarray[:, self.cols] = result
            result = X_ndarray

        # self.cols backup
        self.cols = saved_cols

        return result

    def define_cols(self, X):
        # cast to pandas DataFrame with inferring object types
        if not isinstance(X, pd.DataFrame):
            X_df = pd.DataFrame(X).infer_objects()
        else:
            X_df = X.infer_objects()

        # check all the columns
        numeric_cols = []
        for num, col in enumerate(X_df):
            # if dtype is 'numeric'
            if pd.api.types.is_numeric_dtype(X_df[col]):
                # appending if float
                if pd.api.types.is_float_dtype(X_df[col]):
                    numeric_cols.append(num)
                elif not self.only_float:
                    # checking rated_search
                    if self.rated_search:
                        if X_df[col].nunique() >= self.numeric_rate * X_df.shape[0]:
                            numeric_cols.append(num)
                    else:
                        numeric_cols.append(num)
        return np.array(numeric_cols)

    def cols_to_numeric(self, X):
        if self.cols is None or not self.cols.shape[0]:
            return np.array([])

        inds = self.cols.copy()

        try:
            inds = inds.astype(int)
            return inds
        except (ValueError, TypeError):
            if not isinstance(X, pd.DataFrame):
                return np.array([])
            else:
                columns_array = X.columns.to_numpy(dtype=object).copy()
                names_dict = dict((columns_array[i], i) for i in range(columns_array.shape[0]))
                inds = np.array([names_dict[name] for name in inds if name in names_dict])
                return inds

    def get_cols(self):
        if self.cols is not None:
            return self.cols.copy()
        else:
            return np.array([])

    def get_encoder(self):
        return self.encoder_name

    def get_available_encoders(self):
        return np.array(list(self._encoders_list.keys()))
