from typing import overload
import abc
import typing

import Microsoft.Win32.SafeHandles
import System
import System.ComponentModel
import System.Globalization
import System.Security.Authentication.ExtendedProtection


class ExtendedProtectionPolicyTypeConverter(System.ComponentModel.TypeConverter):
    """This class has no documentation."""

    def can_convert_to(self, context: System.ComponentModel.ITypeDescriptorContext, destination_type: typing.Type) -> bool:
        ...

    def convert_to(self, context: System.ComponentModel.ITypeDescriptorContext, culture: System.Globalization.CultureInfo, value: typing.Any, destination_type: typing.Type) -> System.Object:
        ...


class ChannelBindingKind(System.Enum):
    """This class has no documentation."""

    UNKNOWN = 0

    UNIQUE = ...

    ENDPOINT = ...


class ChannelBinding(Microsoft.Win32.SafeHandles.SafeHandleZeroOrMinusOneIsInvalid, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    @abc.abstractmethod
    def size(self) -> int:
        ...

    @overload
    def __init__(self) -> None:
        """This method is protected."""
        ...

    @overload
    def __init__(self, ownsHandle: bool) -> None:
        """This method is protected."""
        ...


