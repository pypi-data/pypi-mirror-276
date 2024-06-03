from ml_extra.plots.classification import get_roc_curve
from ml_extra.plots.classification import get_precision_recall_curve
from ml_extra.plots.classification import get_confusion_matrix

from ml_extra.loggers.decorators.artifacts import log_figures
from ml_extra.utils.utils import add_prefix_to_dictionary_keys
from ml_extra.utils.utils import add_path_to_dictionary_keys

from typing import Optional
from typing import Tuple
from typing import Union

import pandas as pd
import numpy as np


@log_figures
def log_classification_artifacts(
    y_true: Union[pd.Series, np.ndarray],
    y_pred: Union[pd.Series, np.ndarray],
    prefix: Optional[str] = "",
    artifact_path: Optional[str] = "",
    figsize: Optional[Tuple] = (15, 15),
) -> None:
    """
    Log classification artifacts.
    """
    figure_dict = {
        "roc_curve.png": get_roc_curve(y_true, y_pred, figsize=figsize),
        "precision_recall_curve.png": get_precision_recall_curve(
            y_true, y_pred, figsize=figsize
        ),
        "confusion_matrix.png": get_confusion_matrix(y_true, y_pred, figsize=figsize),
    }

    if prefix:
        figure_dict = add_prefix_to_dictionary_keys(
            dictionary=figure_dict, prefix=prefix
        )
    if artifact_path:
        figure_dict = add_path_to_dictionary_keys(
            dictionary=figure_dict, path=artifact_path
        )

    return figure_dict
