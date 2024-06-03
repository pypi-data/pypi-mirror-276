from .base_estimator import BaseEstimator

class BaseTransformer(BaseEstimator):
    """
    Base class for all transformers.
    """
    def transform(self, data):
        raise NotImplementedError("transform method not implemented")
    
    def fit_transform(self, data):
        self.fit(data)
        return self.transform(data)
