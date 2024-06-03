from typing import Union
from typing import Tuple
from typing import Union
from typing import Any
from typing import Dict
from pathlib import Path
from datetime import datetime


def get_root_path() -> Path:
    """
    Get the root path of the project.
    """
    return Path(__file__).parent.parent.parent


def encode_file(name: Union[Path, str]) -> str:
    """
    Encode a name with a timestamp.

    :param name: Name to encode.
    :return: Encoded name.
    """
    if isinstance(name, str):
        name = Path(name)

    if isinstance(name, Path):
        if not name.suffix:
            raise ValueError("The file must have a suffix.")
    suffix = name.suffix
    name = name.stem
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{name}_{timestamp}{suffix}"


def decode_filename(name: Union[str, Path]) -> Tuple[str, datetime]:
    """
    Return the original name and the date from the encoded name.

    :param name: Encoded name.
    :return: Original name and date.
    """
    if isinstance(name, str):
        filename = Path(name)
    if isinstance(filename, Path):
        name = filename.stem
    name_comp = name.split("_")
    name = "_".join(name_comp[:-1]) + filename.suffix
    timestamp = name_comp[-1]

    timestamp = datetime.strptime(timestamp, "%Y%m%d%H%M%S")
    return name, timestamp


def add_prefix_to_dictionary_keys(
    dictionary: Dict[str, Any], prefix: str
) -> Dict[str, Any]:
    """
    Add a prefix to the keys of a dictionary.

    :param dictionary: Dictionary.
    :param prefix: Prefix to add.
    :return: Dictionary with the prefix.
    """
    return {f"{prefix}_{key}": value for key, value in dictionary.items()}


def add_path_to_dictionary_keys(
    dictionary: Dict[str, Any], path: str
) -> Dict[str, Any]:
    """
    Add a path to the keys of a dictionary.

    :param dictionary: Dictionary.
    :param path: Path to add.
    :return: Dictionary with the path.
    """
    if isinstance(path, Path):
        path = str(path)

    if not path.endswith("/"):
        # add the / at the end
        path = path + "/"

    if path.startswith("/"):
        # remove the / from the start
        path = path[1:]

    return {path + key: value for key, value in dictionary.items()}
