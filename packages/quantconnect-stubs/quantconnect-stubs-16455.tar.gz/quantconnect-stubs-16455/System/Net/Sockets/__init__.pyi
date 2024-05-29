from typing import overload
import typing

import System
import System.ComponentModel
import System.Net.Sockets
import System.Runtime.Serialization


class SocketException(System.ComponentModel.Win32Exception):
    """Provides socket exceptions to the application."""

    @property
    def message(self) -> str:
        ...

    @property
    def socket_error_code(self) -> int:
        """This property contains the int value of a member of the System.Net.Sockets.SocketError enum."""
        ...

    @property
    def error_code(self) -> int:
        ...

    @overload
    def __init__(self, errorCode: int) -> None:
        """Creates a new instance of the System.Net.Sockets.SocketException class with the specified error code."""
        ...

    @overload
    def __init__(self, errorCode: int, message: str) -> None:
        """Initializes a new instance of the System.Net.Sockets.SocketException class with the specified error code and optional message."""
        ...

    @overload
    def __init__(self) -> None:
        """Creates a new instance of the System.Net.Sockets.SocketException class with the default error code."""
        ...

    @overload
    def __init__(self) -> None:
        """Creates a new instance of the System.Net.Sockets.SocketException class with the default error code."""
        ...

    @overload
    def __init__(self, serializationInfo: System.Runtime.Serialization.SerializationInfo, streamingContext: System.Runtime.Serialization.StreamingContext) -> None:
        """
        This method is protected.
        
        Obsoletions.LegacyFormatterImplMessage
        """
        ...


class SocketError(System.Enum):
    """This class has no documentation."""

    SUCCESS = 0

    SOCKET_ERROR = ...

    INTERRUPTED = ...

    ACCESS_DENIED = ...

    FAULT = ...

    INVALID_ARGUMENT = ...

    TOO_MANY_OPEN_SOCKETS = ...

    WOULD_BLOCK = ...

    IN_PROGRESS = ...

    ALREADY_IN_PROGRESS = ...

    NOT_SOCKET = ...

    DESTINATION_ADDRESS_REQUIRED = ...

    MESSAGE_SIZE = ...

    PROTOCOL_TYPE = ...

    PROTOCOL_OPTION = ...

    PROTOCOL_NOT_SUPPORTED = ...

    SOCKET_NOT_SUPPORTED = ...

    OPERATION_NOT_SUPPORTED = ...

    PROTOCOL_FAMILY_NOT_SUPPORTED = ...

    ADDRESS_FAMILY_NOT_SUPPORTED = ...

    ADDRESS_ALREADY_IN_USE = ...

    ADDRESS_NOT_AVAILABLE = ...

    NETWORK_DOWN = ...

    NETWORK_UNREACHABLE = ...

    NETWORK_RESET = ...

    CONNECTION_ABORTED = ...

    CONNECTION_RESET = ...

    NO_BUFFER_SPACE_AVAILABLE = ...

    IS_CONNECTED = ...

    NOT_CONNECTED = ...

    SHUTDOWN = ...

    TIMED_OUT = ...

    CONNECTION_REFUSED = ...

    HOST_DOWN = ...

    HOST_UNREACHABLE = ...

    PROCESS_LIMIT = ...

    SYSTEM_NOT_READY = ...

    VERSION_NOT_SUPPORTED = ...

    NOT_INITIALIZED = ...

    DISCONNECTING = ...

    TYPE_NOT_FOUND = ...

    HOST_NOT_FOUND = ...

    TRY_AGAIN = ...

    NO_RECOVERY = ...

    NO_DATA = ...

    IO_PENDING = ...

    OPERATION_ABORTED = ...


class AddressFamily(System.Enum):
    """Specifies the addressing scheme that an instance of the Socket class can use."""

    UNKNOWN = -1

    UNSPECIFIED = 0

    UNIX = 1

    INTER_NETWORK = 2

    IMP_LINK = 3

    PUP = 4

    CHAOS = 5

    NS = 6

    IPX = ...

    ISO = 7

    OSI = ...

    ECMA = 8

    DATA_KIT = 9

    CCITT = 10

    SNA = 11

    DEC_NET = 12

    DATA_LINK = 13

    LAT = 14

    HYPER_CHANNEL = 15

    APPLE_TALK = 16

    NET_BIOS = 17

    VOICE_VIEW = 18

    FIRE_FOX = 19

    BANYAN = 21

    ATM = 22

    INTER_NETWORK_V_6 = 23

    CLUSTER = 24

    IEEE_12844 = 25

    IRDA = 26

    NETWORK_DESIGNERS = 28

    MAX = 29

    PACKET = 65536

    CONTROLLER_AREA_NETWORK = 65537


