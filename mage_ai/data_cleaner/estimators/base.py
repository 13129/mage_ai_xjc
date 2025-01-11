from sklearn import base


class BaseEstimator(base.BaseEstimator):
    def fit(self, x, y=None):
        return self

    def fit_transform(self, x, y=None):
        self.fit(x, y)
        return self.transform(x)

    def transform(self, x, **kwargs):
        return x
