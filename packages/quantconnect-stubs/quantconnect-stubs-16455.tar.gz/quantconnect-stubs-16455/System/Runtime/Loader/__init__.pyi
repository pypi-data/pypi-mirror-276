from typing import overload
import typing

import System
import System.Collections.Generic
import System.IO
import System.Reflection
import System.Runtime.Loader

System_Runtime_Loader__EventContainer_Callable = typing.TypeVar("System_Runtime_Loader__EventContainer_Callable")
System_Runtime_Loader__EventContainer_ReturnType = typing.TypeVar("System_Runtime_Loader__EventContainer_ReturnType")


class AssemblyDependencyResolver(System.Object):
    """This class has no documentation."""

    @overload
    def __init__(self, componentAssemblyPath: str) -> None:
        ...

    @overload
    def __init__(self, componentAssemblyPath: str) -> None:
        ...

    @overload
    def resolve_assembly_to_path(self, assembly_name: System.Reflection.AssemblyName) -> str:
        ...

    @overload
    def resolve_assembly_to_path(self, assembly_name: System.Reflection.AssemblyName) -> str:
        ...

    @overload
    def resolve_unmanaged_dll_to_path(self, unmanaged_dll_name: str) -> str:
        ...

    @overload
    def resolve_unmanaged_dll_to_path(self, unmanaged_dll_name: str) -> str:
        ...


class AssemblyLoadContext(System.Object):
    """This class has no documentation."""

    class ContextualReflectionScope(System.IDisposable):
        """Opaque disposable struct used to restore CurrentContextualReflectionContext"""

        def dispose(self) -> None:
            ...

    @property
    def assemblies(self) -> System.Collections.Generic.IEnumerable[System.Reflection.Assembly]:
        ...

    @property
    def resolving_unmanaged_dll(self) -> _EventContainer[typing.Callable[[System.Reflection.Assembly, str], System.IntPtr], System.IntPtr]:
        ...

    @property
    def resolving(self) -> _EventContainer[typing.Callable[[System.Runtime.Loader.AssemblyLoadContext, System.Reflection.AssemblyName], System.Reflection.Assembly], System.Reflection.Assembly]:
        ...

    @property
    def unloading(self) -> _EventContainer[typing.Callable[[System.Runtime.Loader.AssemblyLoadContext], None], None]:
        ...

    DEFAULT: System.Runtime.Loader.AssemblyLoadContext

    @property
    def is_collectible(self) -> bool:
        ...

    @property
    def name(self) -> str:
        ...

    ALL: System.Collections.Generic.IEnumerable[System.Runtime.Loader.AssemblyLoadContext]

    CURRENT_CONTEXTUAL_REFLECTION_CONTEXT: System.Runtime.Loader.AssemblyLoadContext
    """Nullable current AssemblyLoadContext used for context sensitive reflection APIs"""

    @overload
    def __init__(self) -> None:
        """This method is protected."""
        ...

    @overload
    def __init__(self, isCollectible: bool) -> None:
        """This method is protected."""
        ...

    @overload
    def __init__(self, name: str, isCollectible: bool = False) -> None:
        ...

    @overload
    def enter_contextual_reflection(self) -> System.Runtime.Loader.AssemblyLoadContext.ContextualReflectionScope:
        """
        Enter scope using this AssemblyLoadContext for ContextualReflection
        
        :returns: A disposable ContextualReflectionScope for use in a using block.
        """
        ...

    @staticmethod
    @overload
    def enter_contextual_reflection(activating: System.Reflection.Assembly) -> System.Runtime.Loader.AssemblyLoadContext.ContextualReflectionScope:
        """
        Enter scope using this AssemblyLoadContext for ContextualReflection
        
        :param activating: Set CurrentContextualReflectionContext to the AssemblyLoadContext which loaded activating.
        :returns: A disposable ContextualReflectionScope for use in a using block.
        """
        ...

    @staticmethod
    def get_assembly_name(assembly_path: str) -> System.Reflection.AssemblyName:
        ...

    @staticmethod
    def get_load_context(assembly: System.Reflection.Assembly) -> System.Runtime.Loader.AssemblyLoadContext:
        ...

    def load(self, assembly_name: System.Reflection.AssemblyName) -> System.Reflection.Assembly:
        """This method is protected."""
        ...

    def load_from_assembly_name(self, assembly_name: System.Reflection.AssemblyName) -> System.Reflection.Assembly:
        ...

    def load_from_assembly_path(self, assembly_path: str) -> System.Reflection.Assembly:
        ...

    def load_from_native_image_path(self, native_image_path: str, assembly_path: str) -> System.Reflection.Assembly:
        ...

    @overload
    def load_from_stream(self, assembly: System.IO.Stream) -> System.Reflection.Assembly:
        ...

    @overload
    def load_from_stream(self, assembly: System.IO.Stream, assembly_symbols: System.IO.Stream) -> System.Reflection.Assembly:
        ...

    def load_unmanaged_dll(self, unmanaged_dll_name: str) -> System.IntPtr:
        """This method is protected."""
        ...

    def load_unmanaged_dll_from_path(self, unmanaged_dll_path: str) -> System.IntPtr:
        """This method is protected."""
        ...

    def set_profile_optimization_root(self, directory_path: str) -> None:
        ...

    def start_profile_optimization(self, profile: str) -> None:
        ...

    def to_string(self) -> str:
        ...

    def unload(self) -> None:
        ...


class _EventContainer(typing.Generic[System_Runtime_Loader__EventContainer_Callable, System_Runtime_Loader__EventContainer_ReturnType]):
    """This class is used to provide accurate autocomplete on events and cannot be imported."""

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> System_Runtime_Loader__EventContainer_ReturnType:
        """Fires the event."""
        ...

    def __iadd__(self, item: System_Runtime_Loader__EventContainer_Callable) -> None:
        """Registers an event handler."""
        ...

    def __isub__(self, item: System_Runtime_Loader__EventContainer_Callable) -> None:
        """Unregisters an event handler."""
        ...


