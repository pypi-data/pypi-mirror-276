"""Punchboot."""


# start delvewheel patch
def _delvewheel_patch_1_6_0():
    import os
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, '.'))
    if os.path.isdir(libs_dir):
        os.add_dll_directory(libs_dir)


_delvewheel_patch_1_6_0()
del _delvewheel_patch_1_6_0
# end delvewheel patch

from _punchboot import (  # type: ignore # noqa: F401
    ArgumentError,
    AuthenticationError,
    CommandError,
    Error,
    GenericError,
    IOError,
    KeyRevokedError,
    MemError,
    NoMemoryError,
    NotAuthenticatedError,
    NotFoundError,
    NotSupportedError,
    PartNotBootableError,
    PartVerifyError,
    SignatureError,
    StreamNotInitializedError,
    TimeoutError,
    TransferError,
)

from .helpers import library_version, list_usb_devices, pb_id, wait_for_device
from .partition import Partition, PartitionFlags
from .session import Session
from .slc import SLC

_pb_exceptions = [
    "Error",
    "GenericError",
    "AuthenticationError",
    "NotAuthenticatedError",
    "NotSupportedError",
    "ArgumentError",
    "CommandError",
    "PartVerifyError",
    "PartNotBootableError",
    "NoMemoryError",
    "TransferError",
    "NotFoundError",
    "StreamNotInitializedError",
    "TimeoutError",
    "KeyRevokedError",
    "SignatureError",
    "MemError",
    "IOError",
]

__all__ = [
    "Session",
    "Partition",
    "PartitionFlags",
    "SLC",
    "library_version",
    "pb_id",
    "wait_for_device",
    "list_usb_devices",
]
__all__ += _pb_exceptions