from typing import overload
import typing

import System
import System.Net.Cache


class RequestCacheLevel(System.Enum):
    """This class has no documentation."""

    DEFAULT = 0

    BYPASS_CACHE = 1

    CACHE_ONLY = 2

    CACHE_IF_AVAILABLE = 3

    REVALIDATE = 4

    RELOAD = 5

    NO_CACHE_NO_STORE = 6


class RequestCachePolicy(System.Object):
    """This class has no documentation."""

    @property
    def level(self) -> int:
        """This property contains the int value of a member of the System.Net.Cache.RequestCacheLevel enum."""
        ...

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, level: System.Net.Cache.RequestCacheLevel) -> None:
        ...

    def to_string(self) -> str:
        ...


