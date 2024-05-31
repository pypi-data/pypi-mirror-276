from copy import deepcopy
from sklearn.base import BaseEstimator, TransformerMixin
import sklearn.preprocessing as skpr
import numpy as np
import pandas as pd
import secrets
import string
from .numerical_encoder import NumericalEncoder
from .datetime_encoder import DateTimeEncoder
from .categorical_encoder import CategoricalEncoder


class Encoder(BaseEstimator, TransformerMixin):
    def __init__(self, categorical_args=None, numerical_args=None, 
                 datetime_args=None, categorical_enabled=True,
                 numerical_enabled=True, datetime_enabled=True, 
                 target_enabled=True, target_encoder='label', 
                 keep_df=False):

        # Target info
        self.target_encoder = target_encoder
        self.target_enabled = target_enabled
        self._target_encoders_list = {'label': skpr.LabelEncoder}
        self._encoder = None
        self.keep_df = keep_df

        # Encoders
        self.categorical_args = categorical_args if categorical_args is not None else dict()
        self.numerical_args = numerical_args if numerical_args is not None else dict()
        self.datetime_args = datetime_args if datetime_args is not None else dict()
        self.categorical_enc = CategoricalEncoder(**self.categorical_args)
        self.numerical_enc = NumericalEncoder(**self.numerical_args)
        self.datetime_enc = DateTimeEncoder(**self.datetime_args)

        # Enabled info
        self.categorical_enabled = categorical_enabled
        self.numerical_enabled = numerical_enabled
        self.datetime_enabled = datetime_enabled
        
        # Missing value placeholder
        self.missing_value = 1e-6

    def fit(self, X, y=None, **fit_params):
        if self.categorical_enabled:
            self.categorical_enc.fit(X, y, **fit_params)
            
        if self.numerical_enabled:
            self.numerical_enc.fit(X, y, **fit_params)

        if self.datetime_enabled:
            self.datetime_enc.fit(X, y, **fit_params)

        if y is not None and (self.target_enabled or not pd.api.types.is_numeric_dtype(y)):
            if self.target_encoder in self._target_encoders_list:
                self._encoder = self._target_encoders_list[self.target_encoder]().fit(y)
            else:
                self._encoder = self._target_encoders_list['label']().fit(y)

        cat_cols = self.cols_to_numeric(X, self.categorical_enc.get_cols())
        num_cols = self.cols_to_numeric(X, self.numerical_enc.get_cols())
        dt_cols = self.cols_to_numeric(X, self.datetime_enc.get_cols())

        if isinstance(X, pd.DataFrame):
            X_columns = X.columns.to_numpy(dtype=object).copy()
            self.categorical_enc.cols = X_columns[cat_cols] if len(cat_cols) > 0 else np.array([])
            self.numerical_enc.cols = X_columns[num_cols] if len(num_cols) > 0 else np.array([])
            self.datetime_enc.cols = X_columns[dt_cols] if len(dt_cols) > 0 else np.array([])

        return self

    def transform(self, X, y=None):
        # target encoding
        y_copy = None
        y_names = None
        if y is not None:
            X_result, y_copy = self.fill_omissions(X, y)
            X_result, y_copy = self.drop_duplicates(X_result, y_copy)
            y_names = pd.DataFrame(y_copy).columns.tolist()
            if self.target_enabled or not pd.api.types.is_numeric_dtype(y_copy):
                if self._encoder is not None:
                    y_copy = self._encoder.transform(y_copy)
                else:
                    y_copy = skpr.LabelEncoder().fit_transform(y_copy)
        else:
            X_result = self.fill_omissions(X)
            
        # main encoding
        if not isinstance(X_result, pd.DataFrame):
            X_result = pd.DataFrame(X_result)
                
        if self.numerical_enabled:
            X_result = self.numerical_enc.transform(X_result, y_copy)

        if self.categorical_enabled:
            X_result = self.categorical_enc.transform(X_result, y_copy)

        if self.datetime_enabled:
            X_result = self.datetime_enc.transform(X_result, y_copy)
            
        if not isinstance(X, pd.DataFrame) or not self.keep_df:
            X_result = X_result.to_numpy()

        if y_names is not None and not isinstance(y, np.ndarray) and self.keep_df:
            y_copy = pd.DataFrame(y_copy, columns=y_names)
        else:
            y_copy = np.squeeze(y_copy)

        # getting the result
        if y_copy is not None and len(y_copy.shape) > 0:
            return X_result, y_copy
        else:
            return X_result

    def fit_transform(self, X, y=None, **fit_params):
        return self.fit(X, y, **fit_params).transform(X, y)

    def fill_omissions(self, X, y=None):

        X_result = deepcopy(X)

        if not isinstance(X_result, pd.DataFrame):
            X_result = pd.DataFrame(X_result)

        # For categories and datetime
        for col_ind in X_result.dtypes[X_result.dtypes == 'category'].index:
            X_result[col_ind] = X_result[col_ind].cat.add_categories([self.missing_value])
            
        X_result.loc[:, self.categorical_enc.get_cols()].fillna(self.missing_value, inplace=True)
        X_result.loc[:, self.datetime_enc.get_cols()].fillna(self.missing_value, inplace=True)
        
        # For numerical features
        for num_col in self.numerical_enc.get_cols():
            X_result.loc[:, num_col].fillna(X_result[num_col].mean(skipna=True), inplace=True)

        if y is not None:
            if not isinstance(y, pd.Series):
                y_result = pd.Series(y)
            else:
                y_result = deepcopy(y)

            return X_result, y_result
        else:
            return X_result

    def drop_duplicates(self, X, y=None, security_len=128):

        X_result = deepcopy(X)

        if not isinstance(X_result, pd.DataFrame):
            X_result = pd.DataFrame(X_result)

        if y is not None:
            if not isinstance(y, pd.Series):
                y_result = pd.Series(y)
            else:
                y_result = deepcopy(y)

            characters = string.ascii_letters + string.digits + string.punctuation
            random_string = ''.join(secrets.choice(characters) for _ in range(security_len))

            X_result[random_string] = y_result
            X_result = X_result.drop_duplicates()
            y_result = X_result[random_string]
            X_result = X_result.drop(random_string, axis=1)

            return X_result, y_result
        else:
            return X_result.drop_duplicates()


    def print_cols(self):
        print('Categorical columns: ', sep=', ', end='')
        print(*self.categorical_enc.get_cols(), sep=', ')
        print('Numerical columns: ', sep=', ', end='')
        print(*self.numerical_enc.get_cols(), sep=', ')
        print('Datetime columns: ', sep=', ', end='')
        print(*self.datetime_enc.get_cols(), sep=', ')

    def cols_to_numeric(self, X, cols):
        if cols is None or not cols.shape[0]:
            return np.array([])

        inds = cols.copy()

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
        return {'categorical': self.categorical_enc.get_cols(),
                'numerical': self.numerical_enc.get_cols(),
                'datetime': self.datetime_enc.get_cols()}
