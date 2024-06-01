from abc import abstractmethod
from typing import Any, BinaryIO, Generic, Protocol, TypeVar

T = TypeVar("T", covariant=True)


class BAREType(Protocol, Generic[T]):
    @abstractmethod
    def pack(self) -> bytes: ...

    @classmethod
    @abstractmethod
    def unpack(cls, fp: BinaryIO) -> T: ...

    @classmethod
    @abstractmethod
    def validate(cls, value: Any) -> bool:
        return False

    @abstractmethod
    def __eq__(cls, other: Any) -> bool:
        return NotImplemented
