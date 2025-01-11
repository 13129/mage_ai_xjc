from collections import OrderedDict

import numpy as np
from sklearn.preprocessing import LabelEncoder

from mage_ai.data_cleaner.estimators.base import BaseEstimator
from mage_ai.shared.conversions import fd_to_df, np_to_fd
from mage_ai.shared.multi import execute_parallel


class CustomLabelEncoder(BaseEstimator):
    def __init__(self):
        self.encoder = LabelEncoder()
        self.fitted = False
        self.label_values = []
        self.unknown_class = None

    def inverse_transform(self, y):
        return self.encoder.inverse_transform(y)

    def fit(self, x, y=None):
        self.encoder.fit(x)
        self.fitted = True
        return self

    def transform(self, x, **kwargs):
        self.label_values = sorted(set(x))
        class_mappings = dict(
            zip(
                [str(c) for c in self.encoder.classes_],
                self.encoder.transform(self.encoder.classes_),
            ),
        )
        missing_value = len(self.encoder.classes_)
        unknown_found = False

        def _build(x):
            v = class_mappings.get(str(x))
            if v is None:
                return missing_value
            return v

        if unknown_found:
            # TODO(christhetree): why are these multiplied by 2?
            if np.issubdtype(x.dtype, np.floating):
                self.unknown_class = float(self.label_values[-1] * 2)
            elif np.issubdtype(x.dtype, np.integer):
                self.unknown_class = int(self.label_values[-1] * 2)
            else:
                self.unknown_class = 'unknown_class_'
        y = np.array([_build(x) for x in x])
        return y

    def label_classes(self):
        if self.unknown_class:
            return self.encoder.classes_ + [self.unknown_class]
        return self.encoder.classes_


class MultipleColumnLabelEncoder(BaseEstimator):
    def __init__(self, input_type=None):
        self.input_type = input_type
        self.encoders = {}

    def fit(self, x, y=None):
        execute_parallel(
            [(self.fit_column, [x[column], column]) for column in x.columns],
        )
        return self

    def fit_column(self, x, column):
        self.encoders[column] = CustomLabelEncoder()
        if self.input_type:
            self.encoders[column].fit(x.apply(self.input_type))
        else:
            self.encoders[column].fit(x)

    def transform(self, x, parallel=False):
        if parallel:
            output_dict = OrderedDict()
            output_dicts = execute_parallel(
                [(self.transform_column, [x[column], column]) for column in x.columns],
            )

            for od in output_dicts:
                output_dict.update(od)
            return fd_to_df(output_dict)

        x_output = x.copy(deep=True)
        for col in x_output.columns:
            if self.input_type:
                x_output[col] = self.encoders[col].transform(
                    x_output[col].apply(self.input_type),
                )
            else:
                x_output[col] = self.encoders[col].transform(x_output[col])
        return x_output

    def transform_column(self, x, column):
        if self.input_type:
            nd_arr = self.encoders[column].transform(x.apply(self.input_type))
        else:
            nd_arr = self.encoders[column].transform(x)
        return np_to_fd(nd_arr, feature_names=[column])
