class BaseMetric:
    """
    Base class for all metrics.
    """
    def compute(self, y_true, y_pred):
        raise NotImplementedError("compute method not implemented")
