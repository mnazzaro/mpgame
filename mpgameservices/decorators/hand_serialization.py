from typing import Callable, Any
from functools import wraps


def provide_hand (f: Callable) -> Callable:
    @wraps(f)
    def wrapper (*args: Any, **kwargs: Any):
        ...
    return wrapper
            