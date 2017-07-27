import pickle
from typing import Any

def dump_data_object(obj: Any, path: str) -> None:
    """This function serialize ``obj`` and save it to ``path``

    Args:
        obj (Any): any serializable object(something like list, dataframe, dict, ...)

    Returns:
        None
    """

    with open(path, 'wb') as handle:
        pickle.dump(obj, handle)


def load_data_object(path: str) -> Any:
    """This function open the file in specified path and
     return cooresponding data object

    Args:
        path (path): any

    Returns:
        Any: a python object(something like list, dataframe, dict, ...)
    """
    with open(path, 'rb') as handle:
        data = pickle.load(handle)

    return data
