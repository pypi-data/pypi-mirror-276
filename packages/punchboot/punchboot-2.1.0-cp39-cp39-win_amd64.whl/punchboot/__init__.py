"""Punchboot."""


# start delvewheel patch
def _delvewheel_patch_1_6_0():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, '.'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-punchboot-2.1.0')
        if os.path.isfile(load_order_filepath):
            with open(os.path.join(libs_dir, '.load-order-punchboot-2.1.0')) as file:
                load_order = file.read().split()
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
                if os.path.isfile(lib_path) and not kernel32.LoadLibraryExW(ctypes.c_wchar_p(lib_path), None, 0x00000008):
                    raise OSError('Error loading {}; {}'.format(lib, ctypes.FormatError(ctypes.get_last_error())))


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