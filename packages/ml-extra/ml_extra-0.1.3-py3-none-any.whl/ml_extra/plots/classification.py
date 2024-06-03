from ml_extra.plots.validations import __check_binary_classification

from typing import Optional
from typing import Tuple
from typing import Union

import numpy as np
import pandas as pd
from sklearn.metrics import RocCurveDisplay
from sklearn.metrics import PrecisionRecallDisplay
from sklearn.metrics import ConfusionMatrixDisplay

import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def get_roc_curve(
    y_true: Union[pd.Series, np.ndarray],
    y_pred: Union[pd.Series, np.ndarray],
    figsize: Optional[Tuple] = (15, 5),
    name: Optional[str] = "Classifier",
) -> Figure:
    """
    Get the ROC curve.

    :param y_true: True labels.
    :param y_pred: Predicted labels.
    :param figsize: Figure size.
    :param name: Classifier name.
    :return: The ROC curve figure.
    """
    __check_binary_classification(y_true, y_pred)

    plt.figure(figsize=figsize)
    roc_display = RocCurveDisplay.from_predictions(
        y_true, y_pred, name=name, ax=plt.gca()
    )
    return roc_display.figure_


def get_precision_recall_curve(
    y_true: Union[pd.Series, np.ndarray],
    y_pred: Union[pd.Series, np.ndarray],
    figsize: Optional[Tuple] = (15, 5),
    name: Optional[str] = "Classifier",
) -> Figure:
    """
    Get the precision-recall curve.

    :param y_true: True labels.
    :param y_pred: Predicted labels.
    :param figsize: Figure size.
    :param name: Classifier name.
    :return: The precision-recall curve figure.
    """
    __check_binary_classification(y_true, y_pred)

    plt.figure(figsize=figsize)
    pr_display = PrecisionRecallDisplay.from_predictions(
        y_true, y_pred, name=name, ax=plt.gca()
    )
    return pr_display.figure_


def get_confusion_matrix(
    y_true: Union[pd.Series, np.ndarray],
    y_pred: Union[pd.Series, np.ndarray],
    figsize: Optional[Tuple] = (15, 5),
    name: Optional[str] = "Classifier",
) -> Figure:
    """
    Get the confusion matrix.

    :param y_true: True labels.
    :param y_pred: Predicted labels.
    :param figsize: Figure size.
    :param name: Classifier name.
    :return: The confusion matrix figure.
    """
    __check_binary_classification(y_true, y_pred)

    plt.figure(figsize=figsize)
    cm_display = ConfusionMatrixDisplay.from_predictions(y_true, y_pred, ax=plt.gca())
    return cm_display.figure_
