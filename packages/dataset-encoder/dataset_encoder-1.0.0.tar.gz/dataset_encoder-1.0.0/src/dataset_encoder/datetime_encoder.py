from .circular_encoder import CircularEncoder
import math
from copy import deepcopy
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import pandas as pd


class DateTimeEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, cols=None, fit_replace=True,
                 drop=True, min_rescale=True, fast_mode=True,
                 confidence_level=0.99, worst_proportion=0.01):
        self.cols = np.array(cols) if cols is not None else None
        self.fit_replace = fit_replace
        self.drop = drop
        self.min_rescale = min_rescale

        # stochastic approach
        eps = 1e-6
        confidence_level = max(eps, min(confidence_level, 1 - eps))
        worst_proportion = max(eps, min(worst_proportion, 1 - eps))
        self.fast_random_size = math.ceil(math.log(1 - confidence_level) / math.log(1 - worst_proportion))
        self.fast_mode = fast_mode

        # encoders for months, days and hours
        self.encoders = {'months': CircularEncoder(limits=[12], fit_replace=False),
                         'days': CircularEncoder(limits=[30], fit_replace=False),
                         'hours': CircularEncoder(limits=[24], fit_replace=False)}

    def __repr__(self):
        return "DateTimeEncoder"

    def __str__(self):
        return "DateTimeEncoder"

    def fit(self, X, y=None):
        if self.cols is None or self.fit_replace:
            if self.fast_mode and self.fast_random_size < X.shape[0]:
                self.cols = self.define_cols_fast(X)
            else:
                self.cols = self.define_cols(X)

        return self

    def transform(self, X, y=None):
        try:
            if self.cols is None or not self.cols.shape[0]:
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

        # cast to pandas DataFrame
        if isinstance(X, pd.DataFrame):
            column_names = X.columns.to_numpy(dtype=object).copy()
            X_df = X
        else:
            X_df = pd.DataFrame(X)

        # shift for dropping columns
        shift = 0 if self.drop else 1

        # creating an empty result matrix
        result = np.zeros((X_df.shape[0], X_df.shape[1] + (6 + shift) * len(self.cols)), dtype=object)
        column_names_zeros = np.zeros(X_df.shape[1] + (6 + shift) * len(self.cols), dtype=object)

        # creating indices for fast numpy operation
        modified_inds = np.array([self.cols[i] + i * (6 + shift) for i in range(len(self.cols))])
        not_cols = list(set(np.arange(X.shape[1])) - set(self.cols))
        unmodified_inds = np.array([i + (7 + shift) * (not_cols[i] - i) for i in range(len(not_cols))])

        # setting not date columns
        if unmodified_inds.shape[0] > 0:
            result[:, unmodified_inds] = X_df.to_numpy()[:, not_cols]
            if not self.drop:
                result[:, modified_inds] = X_df.to_numpy()[:, self.cols]
            if column_names is not None:
                column_names_zeros[unmodified_inds] = column_names[not_cols]
                if not self.drop:
                    column_names_zeros[modified_inds] = column_names[self.cols]

        # for fast mode
        preventive_delete = []

        # tranform each datetime column
        for num, col in enumerate(self.cols):
            transformed_column = self.column_transform(X_df.iloc[:, col])
            # for fast mode
            if transformed_column is None:
                result[:, modified_inds[num] + 6 + shift] = X_df.iloc[:, col]
                column_names_zeros[modified_inds[num] + 6 + shift] = X_df.iloc[:, col].name
                preventive_delete += list(np.arange(modified_inds[num] + shift, modified_inds[num] + 6 + shift))
                continue
            result[:, np.arange(modified_inds[num] + shift, modified_inds[num] + 7 + shift)] = transformed_column.to_numpy()
            column_names_zeros[np.arange(modified_inds[num] + shift, modified_inds[num] + 7 + shift)] = transformed_column.columns.to_numpy(dtype=object).copy()

        # delete unsuccessful transformations
        if len(preventive_delete) > 0:
            result = np.delete(result, preventive_delete, 1)
            column_names_zeros = np.delete(column_names_zeros, preventive_delete)

        # self.cols backup
        self.cols = saved_cols

        if column_names is not None:
            # saving dtypes
            saved_dtypes = X_df.dtypes.to_dict()
            unmodified_dtypes = dict([(X.columns[col], saved_dtypes[X.columns[col]]) for col in not_cols])

            return pd.DataFrame(result, columns=column_names_zeros).infer_objects().astype(dtype=unmodified_dtypes)
        else:
            return result

    def column_transform(self, column):
        column_name = None

        # cast to pandas Series
        if not isinstance(column, pd.Series):
            pd_column = deepcopy(pd.Series(column))
        else:
            pd_column = deepcopy(column)
            column_name = column.name

        try:
            pd_column = pd.to_datetime(pd_column.astype(str))
        except (ValueError, TypeError):
            return None

        # rescaling by the start time
        if self.min_rescale:
            pd_column = pd_column.astype(int)
            min_seconds = pd_column.min()
            pd_column = pd_column.apply(lambda val: val - min_seconds)
            pd_column = pd.to_datetime(pd_column)

        # defining main columns
        years = pd_column.dt.year.to_numpy()
        months = self.encoders['months'].fit_transform(pd_column.dt.month.to_numpy())
        days = self.encoders['days'].fit_transform(pd_column.dt.day.to_numpy())
        hours = self.encoders['hours'].fit_transform(pd_column.dt.hour.to_numpy())
        result = np.array([years, months.T[0], months.T[1], days.T[0],
                           days.T[1], hours.T[0], hours.T[1]]).T

        # cast to the original type
        if column_name is not None:
            column_names = np.array([f'{column_name}_year', f'{column_name}_month_sin',
                                     f'{column_name}_month_cos', f'{column_name}_day_sin',
                                     f'{column_name}_day_cos', f'{column_name}_hour_sin',
                                     f'{column_name}_hour_cos'])
            result = pd.DataFrame(result, columns=column_names).infer_objects()

        return result

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
        # cast to pandas DataFrame
        if isinstance(X, pd.DataFrame):
            X_df = X
        else:
            X_df = pd.DataFrame(X)

        # check all the columns
        datetime_cols = []
        for num, col in enumerate(X_df):
            if not pd.api.types.is_categorical_dtype(X_df[col]) and not pd.api.types.is_numeric_dtype(X_df[col]):
                if self.is_datetime(X_df[col].iloc[np.random.randint(0, X_df.shape[0])]):
                    datetime_cols.append(num)
        return np.array(datetime_cols)

    def define_cols_fast(self, X):
        # cast to pandas DataFrame
        if isinstance(X, pd.DataFrame):
            X_df = X
        else:
            X_df = pd.DataFrame(X)

        # check all the columns
        datetime_cols = []
        for num, col in enumerate(X_df):
            if not pd.api.types.is_categorical_dtype(X_df[col]) and not pd.api.types.is_numeric_dtype(X_df[col]):
                append_need = True
                for i in range(self.fast_random_size):
                    if not self.is_datetime(X_df[col].iloc[np.random.randint(0, X_df.shape[0])]):
                        append_need = False
                        break
                if append_need:
                    datetime_cols.append(num)
        return np.array(datetime_cols)

    def get_cols(self):
        if self.cols is not None:
            return self.cols.copy()
        else:
            return np.array([])

    def is_datetime(self, col):
        arg = None
        if not isinstance(col, pd.Series):
            arg = col
        else:
            arg = col.astype(str)

        try:
            pd.to_datetime(arg, errors='raise')
            return True
        except (ValueError, TypeError):
            return False
