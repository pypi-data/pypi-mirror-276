from abc import ABC, abstractmethod
from collections.abc import Callable
from functools import partial
from types import MappingProxyType
from typing import Final, Self, assert_never, cast, override

from pymem.pattern import pattern_scan_all, pattern_scan_module
from pymem.process import module_from_name
from pymem.ressources.kernel32 import SetLastError, VirtualAllocEx
from pymem.ressources.structure import MEMORY_PROTECTION, MEMORY_STATE

from trainerbase.process import _pm as pm


ARCH: Final[int] = 64 if pm.is_64_bit else 32
POINTER_SIZE: Final[int] = 8 if pm.is_64_bit else 4


type ConvertibleToAddress = AbstractAddress | int | bytes | str


read_pointer = cast(Callable[[int], int], pm.read_ulonglong if pm.is_64_bit else pm.read_uint)

__set_last_error = cast(Callable[[int], None], SetLastError)
__virtual_alloc_ex = cast(Callable[..., int], VirtualAllocEx)


class AbstractAddress(ABC):
    @abstractmethod
    def resolve(self) -> int:
        pass


class AOBScan(AbstractAddress):
    # Constant from re. Like re._special_chars_map, but without dot (`.`).
    _SPECIAL_CHARS_MAP = MappingProxyType({i: "\\" + chr(i) for i in b"()[]{}?*+-|^$\\&~# \t\n\r\v\f"})

    def __init__(
        self,
        aob: bytes | str,
        *,
        add: int = 0,
        module_name: str | None = None,
        multiple_result_index: int | None = None,
        should_cache: bool = True,
        should_escape: bool = True,
        any_byte_marker: str = "??",
    ):
        self._should_cache = should_cache
        self._saved_scan_result: int | None = None

        if isinstance(aob, str):
            aob = bytes.fromhex(aob.replace(any_byte_marker, "2E"))  # 2E is hex(46), 46 is ord(".")

        if should_escape:
            aob = self._escape_aob(aob)

        self.aob = aob
        self.add = add
        self.module_name = module_name
        self.multiple_result_index = multiple_result_index

    def __add__(self, extra_add: int) -> Self:
        new_add = self.add + extra_add
        return self.inherit(new_add=new_add)

    @override
    def resolve(self) -> int:
        if self._saved_scan_result is not None:
            return self._saved_scan_result

        return_multiple = self.multiple_result_index is not None

        if self.module_name is None:
            find_aob = partial(pattern_scan_all, pm.process_handle, return_multiple=return_multiple)
        else:
            module = module_from_name(pm.process_handle, self.module_name)

            if module is None:
                raise ValueError(f"Module not found: {self.module_name}")

            find_aob = partial(pattern_scan_module, pm.process_handle, module, return_multiple=return_multiple)

        scan_result: list[int] | int | None = find_aob(self.aob)

        if not scan_result:
            raise ValueError(f"AOB not found: {self.aob}")

        if isinstance(scan_result, list):
            result_address = scan_result[cast(int, self.multiple_result_index)]
        else:
            result_address = scan_result

        result_address += self.add

        if self._should_cache:
            self._saved_scan_result = result_address

        return result_address

    def inherit(self, *, new_add: int | None = None) -> Self:
        new_address = self.__class__(
            self.aob,
            add=self.add,
            module_name=self.module_name,
            multiple_result_index=self.multiple_result_index,
            should_cache=self._should_cache,
        )

        if new_add is not None:
            new_address.add = new_add

        return new_address

    @classmethod
    def _escape_aob(cls, pattern: bytes) -> bytes:
        """
        Escape special characters in a string.

        Forked re.escape. Simplified. Only for bytes.
        """

        return pattern.decode("latin1").translate(cls._SPECIAL_CHARS_MAP).encode("latin1")


class Address(AbstractAddress):
    def __init__(self, base_address: int, offsets: list[int] | None = None, add: int = 0):
        self.base_address = base_address
        self.offsets = [] if offsets is None else offsets
        self.add = add

    def __add__(self, other: int | list[int]) -> Self:
        match other:
            case int(extra_add):
                new_add = self.add + extra_add
                return self.inherit(new_add=new_add)
            case list(extra_offsets):
                return self.inherit(extra_offsets=extra_offsets)
            case _:
                assert_never(other)

    @override
    def resolve(self) -> int:
        pointer = self.base_address
        for offset in self.offsets:
            pointer = read_pointer(pointer) + offset

        return pointer + self.add

    def inherit(self, *, extra_offsets: list[int] | None = None, new_add: int | None = None) -> Self:
        new_address = self.__class__(self.base_address, self.offsets.copy(), self.add)

        if extra_offsets is not None:
            new_address.offsets.extend(extra_offsets)

        if new_add is not None:
            new_address.add = new_add

        return new_address


def ensure_address(obj: ConvertibleToAddress) -> AbstractAddress:
    match obj:
        case AbstractAddress():
            return obj
        case int():
            return Address(obj)
        case bytes() | str():
            return AOBScan(obj)
        case _:
            raise TypeError(f"Cannot create AbstractAddress from {type(obj)}")


def allocate(size: int = POINTER_SIZE, count: int = 1, nearest_to: int | None = None) -> int:
    return __pm_allocate_memory(cast(int, pm.process_handle), size * count, nearest_to)


def get_module_address(module_name: str) -> int:
    """
    Returns 0 if module is not found else module address
    """

    module_info = module_from_name(pm.process_handle, module_name)

    if module_info is None:
        return 0

    return module_info.lpBaseOfDll


def __pm_allocate_memory(
    handle: int,
    size: int,
    nearest_to: int | None = None,
    allocation_type: MEMORY_STATE | None = None,
    protection_type: MEMORY_PROTECTION | None = None,
):
    """
    Pymem fork.

    Reserves or commits a region of memory within the virtual address space of a specified process.
    The function initializes the memory it allocates to zero, unless MEM_RESET is used.

    https://msdn.microsoft.com/en-us/library/windows/desktop/aa366890%28v=vs.85%29.aspx
    """

    if allocation_type is None:
        allocation_type = MEMORY_STATE.MEM_COMMIT

    if protection_type is None:
        protection_type = MEMORY_PROTECTION.PAGE_EXECUTE_READWRITE

    __set_last_error(0)

    address = __virtual_alloc_ex(handle, nearest_to, size, allocation_type.value, protection_type.value)

    return address
