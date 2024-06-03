from .base_estimator import BaseEstimator

class BaseSelection(BaseEstimator):
    """
    Base class for model selection.
    """
    def select(self, data):
        raise NotImplementedError("select method not implemented")
