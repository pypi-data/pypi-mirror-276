from ml_extra.loggers.decorators.utils import check_run
from ml_extra.loggers.decorators.utils import check_valid_json
from ml_extra.loggers.decorators.utils import get_valid_artifact_path_for_json
from ml_extra.loggers.decorators.utils import get_valid_artifact_path_for_yaml

from functools import wraps
from inspect import isfunction

import mlflow


def log_figures(func):
    """
    Log the figures returned by the decorated function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not check_run():
            return func(*args, **kwargs)

        result = func(*args, **kwargs)

        for name, fig in result.items():
            mlflow.log_figure(fig, name)

        return result

    return wrapper


def log_yaml(artifact_path: str):
    """
    Log the dictionary returned by the decorated function as a yaml file.

    :param artifact_path: The artifact path.
    """
    if artifact_path and not isfunction(artifact_path):
        artifact_path = get_valid_artifact_path_for_yaml(artifact_path)
    else:
        raise ValueError("artifact_path is required")

    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not check_run():
                return func(*args, **kwargs)

            result = func(*args, **kwargs)

            mlflow.log_dict(result, artifact_path)
            return result

        return wrapper

    return inner

def log_json(artifact_path: str):
    """
    Log the dictionary returned by the decorated function as a json file.

    :param  artifact_path: The path to the artifact.
    """
    if artifact_path and not isfunction(artifact_path):
        artifact_path = get_valid_artifact_path_for_json(artifact_path)
    else:
        raise ValueError("artifact_path is required")

    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not check_run():
                return func(*args, **kwargs)

            result = func(*args, **kwargs)
            if not check_valid_json(result):
                raise ValueError("The returned object is not a valid json object.")
            
            mlflow.log_dict(result, artifact_path)
            return result

        return wrapper

    return inner