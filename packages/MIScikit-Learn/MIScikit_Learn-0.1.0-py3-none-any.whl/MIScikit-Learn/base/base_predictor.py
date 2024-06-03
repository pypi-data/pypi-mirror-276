from .base_estimator import BaseEstimator

class BasePredictor(BaseEstimator):
    """
    Base class for all predictors.
    """
    def predict(self, data):
        raise NotImplementedError("predict method not implemented")
    
    def predict_proba(self, data):
        raise NotImplementedError("predict_proba method not implemented")
