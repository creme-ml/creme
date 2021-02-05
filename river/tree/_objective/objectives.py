import math
from abc import ABCMeta

from .._utils import GradHess


class BaseObjective(metaclass=ABCMeta):
    """ Base class to implement optimization objectives used in Streaming Gradient Trees. """

    def compute_derivatives(self, y_true: float, y_pred: float) -> GradHess:
        """ Return the gradient and hessian data concerning one instance and its prediction.

        Parameters
        ----------
        y
            Target value.
        y_pred
            Predicted target value.
        """
        pass

    def transfer(self, y: float) -> float:
        """ Optionally apply some transformation to the value predicted by the tree before
        returning it.

        For instance, in classification, the softmax operation might be applied.

        Parameters
        ----------
        y
            Value to be transformed.
        """
        return y


class BinaryCrossEntropyObjective(BaseObjective):
    """ Loss function used in binary classification tasks. """

    def compute_derivatives(self, y_true, y_pred):
        y_trs = self.transfer(y_pred)

        return GradHess(y_trs - y_true, y_trs * (1.0 - y_trs))

    def transfer(self, y):
        return 1.0 / (1.0 + math.exp(-y))


class SquaredErrorObjective(BaseObjective):
    """ Loss function used in regression tasks. """

    def compute_derivatives(self, y_true, y_pred):
        return GradHess(y_pred - y_true, 1.0)