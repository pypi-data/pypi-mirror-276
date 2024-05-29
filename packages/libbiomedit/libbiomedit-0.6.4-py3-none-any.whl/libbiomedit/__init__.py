from typing import Optional, TypeVar

from .version import __version__  # noqa: F401 unused-import

T = TypeVar("T")


def unwrap(opt: Optional[T]) -> T:
    if opt is None:
        raise ValueError("Should not be None")
    return opt
