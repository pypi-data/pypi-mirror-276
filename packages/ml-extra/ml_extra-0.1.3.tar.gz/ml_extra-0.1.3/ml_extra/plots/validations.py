import numpy as np


def __check_binary_classification(y_true, y_pred):
    """
    Check if the input is a binary classification problem.

    :param y_true: True labels.
    :param y_pred: Predicted labels.
    :return: None.
    """
    if len(np.unique(y_true)) != 2 or len(np.unique(y_pred)) != 2:
        raise ValueError("This function only supports binary classification problems.")
