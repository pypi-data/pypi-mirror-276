from typing import overload
import typing

import Internal
import System


class Console(System.Object):
    """This class has no documentation."""

    class Error(System.Object):
        """This class has no documentation."""

        @staticmethod
        @overload
        def write(s: str) -> None:
            ...

        @staticmethod
        @overload
        def write(s: str) -> None:
            ...

        @staticmethod
        @overload
        def write(s: str) -> None:
            ...

        @staticmethod
        @overload
        def write(s: str) -> None:
            ...

        @staticmethod
        def write_line() -> None:
            ...

    @staticmethod
    @overload
    def write(s: str) -> None:
        ...

    @staticmethod
    @overload
    def write(s: str) -> None:
        ...

    @staticmethod
    @overload
    def write(s: str) -> None:
        ...

    @staticmethod
    @overload
    def write(s: str) -> None:
        ...

    @staticmethod
    @overload
    def write_line(s: str) -> None:
        ...

    @staticmethod
    @overload
    def write_line() -> None:
        ...


