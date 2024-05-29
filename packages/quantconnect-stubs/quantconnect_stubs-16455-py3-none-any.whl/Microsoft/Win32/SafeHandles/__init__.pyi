from typing import overload
import abc
import typing

import Microsoft.Win32.SafeHandles
import System
import System.Runtime.InteropServices


class SafeHandleZeroOrMinusOneIsInvalid(System.Runtime.InteropServices.SafeHandle, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def is_invalid(self) -> bool:
        ...

    def __init__(self, ownsHandle: bool) -> None:
        """This method is protected."""
        ...


class SafeFileHandle(Microsoft.Win32.SafeHandles.SafeHandleZeroOrMinusOneIsInvalid):
    """This class has no documentation."""

    @property
    def is_async(self) -> bool:
        ...

    @property
    def is_invalid(self) -> bool:
        ...

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, preexistingHandle: System.IntPtr, ownsHandle: bool) -> None:
        """
        Creates a Microsoft.Win32.SafeHandles.SafeFileHandle around a file handle.
        
        :param preexistingHandle: Handle to wrap
        :param ownsHandle: Whether to control the handle lifetime
        """
        ...

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def release_handle(self) -> bool:
        """This method is protected."""
        ...

    @overload
    def release_handle(self) -> bool:
        """This method is protected."""
        ...


class SafeHandleMinusOneIsInvalid(System.Runtime.InteropServices.SafeHandle, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def is_invalid(self) -> bool:
        ...

    def __init__(self, ownsHandle: bool) -> None:
        """This method is protected."""
        ...


class CriticalHandleMinusOneIsInvalid(System.Runtime.InteropServices.CriticalHandle, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def is_invalid(self) -> bool:
        ...

    def __init__(self) -> None:
        """This method is protected."""
        ...


class SafeWaitHandle(Microsoft.Win32.SafeHandles.SafeHandleZeroOrMinusOneIsInvalid):
    """This class has no documentation."""

    @overload
    def __init__(self) -> None:
        """Creates a Microsoft.Win32.SafeHandles.SafeWaitHandle."""
        ...

    @overload
    def __init__(self, existingHandle: System.IntPtr, ownsHandle: bool) -> None:
        """
        Creates a Microsoft.Win32.SafeHandles.SafeWaitHandle around a wait handle.
        
        :param existingHandle: Handle to wrap
        :param ownsHandle: Whether to control the handle lifetime
        """
        ...

    @overload
    def release_handle(self) -> bool:
        """This method is protected."""
        ...

    @overload
    def release_handle(self) -> bool:
        """This method is protected."""
        ...


class CriticalHandleZeroOrMinusOneIsInvalid(System.Runtime.InteropServices.CriticalHandle, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def is_invalid(self) -> bool:
        ...

    def __init__(self) -> None:
        """This method is protected."""
        ...


