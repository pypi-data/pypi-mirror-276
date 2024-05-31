import math
from copy import deepcopy
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import pandas as pd
import category_encoders as ce
import sklearn.preprocessing as skpr


class CategoricalEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, cols=None, fit_replace=True, encoder='binary',
                 category_rate=0.1, target_related=True, rated_search=True, fast_mode=True,
                 confidence_level=0.99, worst_proportion=0.01, **encoder_params):

        self._hashing_enc_name = 'hashing'
        self._encoders_list = {'onehot': ce.OneHotEncoder,
                               'target_loo': ce.LeaveOneOutEncoder,
                               self._hashing_enc_name: ce.HashingEncoder,
                               'binary': ce.BinaryEncoder,
                               'mestimate': ce.MEstimateEncoder,
                               'glmm': ce.GLMMEncoder,
                               'ordinal': ce.OrdinalEncoder}
        self._target_encoders_list = np.array(['target_loo', 'backward_difference', 
                                               'mestimate', 'glmm'])
        
        self.target_default = 'target_loo'

        # stochastic approach
        eps = 1e-6
        confidence_level = max(eps, min(confidence_level, 1 - eps))
        worst_proportion = max(eps, min(worst_proportion, 1 - eps))
        self.fast_random_size = math.ceil(math.log(1 - confidence_level) / math.log(1 - worst_proportion))
        self.fast_mode = fast_mode

        self.cols = np.array(cols) if cols is not None else None
        self.fit_replace = fit_replace
        self.encoder_name = encoder
        self.category_rate = category_rate
        self.rated_search = rated_search
        self.encoder_params = encoder_params
        self._encoder = None
        self.target_related = target_related

    def __repr__(self):
        return "CategoricalEncoder"

    def __str__(self):
        return "CategoricalEncoder"

    def fit(self, X, y=None, **fit_params):
        if y is not None and self.target_related and self.encoder_name not in self._target_encoders_list:
            self.encoder_name = self.target_default
            
        # defining categorical columns
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
        self.encoder_params['cols'] = X.columns[self.cols] if isinstance(X, pd.DataFrame) else self.cols
        self._encoder = self._encoders_list[self.encoder_name](**self.encoder_params)

        # transforming y if it's not numeric
        y_copy = None

        if y is not None:
            y_copy = deepcopy(y)
            if not self.is_y_approved(y_copy):
                y_copy = skpr.LabelEncoder().fit_transform(y_copy)
            else:
                y_copy = y_copy.astype(float)
            
        # fitting the encoder
        self._encoder.fit(pd.DataFrame(X), y_copy, **fit_params)
        
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

        # transforming y if it's not numeric
        y_copy = None

        if y is not None:
            y_copy = deepcopy(y)
            if not self.is_y_approved(y_copy):
                y_copy = skpr.LabelEncoder().fit_transform(y_copy)

        # checking whether it's a target encoder or not
        if self.encoder_name in self._target_encoders_list:
            result = self._encoder.transform(pd.DataFrame(X), y_copy, override_return_df=True)
        else:
            result = self._encoder.transform(pd.DataFrame(X), override_return_df=True)

        # adjusting the column names
        cols_before = self._encoder.get_feature_names_in()
        cols_after = self._encoder.get_feature_names_out()
        new_columns = self._rename_transformed_cols(cols_before, cols_after)

        result = result.rename(columns={cols_after[i]: new_columns[i] for i in range(cols_after.shape[0])})

        if isinstance(X, pd.DataFrame):
            # saving X dtypes
            not_cols = list(set(np.arange(X.shape[1])) - set(self.cols))
            saved_dtypes = X.dtypes.to_dict()
            unmodified_dtypes = dict([(X.columns[col], saved_dtypes[X.columns[col]]) for col in not_cols])

            # self.cols backup
            self.cols = saved_cols

            return result.astype(dtype=unmodified_dtypes)
        else:
            # self.cols backup
            self.cols = saved_cols

            return result.to_numpy()

    def fit_transform(self, X, y=None, **fit_params):
        # transforming y if it's not numeric
        y_copy = None

        if y is not None:
            y_copy = deepcopy(y)
            if not self.is_y_approved(y_copy):
                y_copy = skpr.LabelEncoder().fit_transform(y_copy)

        self.fit(X, y_copy, **fit_params)
        return self.transform(X, y_copy)

    def _rename_transformed_cols(self, before, after):
        if after is None:
            return np.array([])
        if self._encoder is None:
            return deepcopy(after)

        result = deepcopy(after)

        # hashing encoder unique renaming
        if self.encoder_name == self._hashing_enc_name:
            for i in range(self._encoder.n_components):
                result[i] = f'{self._hashing_enc_name}_{i}'
        else:
            # getting the columns transformed
            set_before = set(before)
            set_after = set(after)
            sample_names = set_before.intersection(set_after)

            # checking whether set is not empty
            if self.encoder_name in self._target_encoders_list:
                for num, col in enumerate(result):
                    if num in self.cols:
                        result[num] = f'{self.encoder_name}_{result[num]}'
            elif bool(sample_names):
                # renaming
                for num, col in enumerate(result):
                    if col not in sample_names:
                        result[num] = f'{self.encoder_name}_{result[num]}'

        return result

    def is_y_approved(self, y):
        return pd.api.types.is_numeric_dtype(y)

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

    def define_cols(self, X):
        # cast to pandas DataFrame with inferring object types
        if not isinstance(X, pd.DataFrame):
            X_df = pd.DataFrame(X).infer_objects()
        else:
            X_df = X.infer_objects()

        # check all the columns
        category_cols = []
        for num, col in enumerate(X_df):
            # if dtype is 'category'
            if pd.api.types.is_categorical_dtype(X_df[col]):
                category_cols.append(num)
            # checking object type (strings)
            elif pd.api.types.is_object_dtype(X_df[col]):
                # stochastic approach
                if self.fast_mode:
                    append_need = True
                    for i in range(self.fast_random_size):
                        if not self.is_one_word(X_df[col].iloc[np.random.randint(0, X_df.shape[0])]):
                            append_need = False
                            break
                    if append_need:
                        category_cols.append(num)
                else:
                    # basic approach
                    if np.all(np.vectorize(self.is_one_word)(X_df[col])):
                        category_cols.append(num)
            # checking numeric columns
            elif self.rated_search and pd.api.types.is_numeric_dtype(X_df[col]) and not pd.api.types.is_float_dtype(X_df[col]):
                if X_df[col].nunique() < self.category_rate * X_df.shape[0]:
                    category_cols.append(num)
        return np.array(category_cols)

    def is_one_word(self, s):
        if s is None or not isinstance(s, str):
            return False

        stripped_string = s.strip()
        if not stripped_string or ' ' in stripped_string:
            return False
        else:
            return True

    def get_cols(self):
        if self.cols is not None:
            return self.cols.copy()
        else:
            return np.array([])

    def get_encoder(self):
        return self.encoder_name

    def get_available_encoders(self):
        return np.array(list(self._encoders_list.keys()))
