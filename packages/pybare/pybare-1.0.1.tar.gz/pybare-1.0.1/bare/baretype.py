from abc import abstractmethod
from io import BytesIO
from typing import (
    Any,
    BinaryIO,
    ByteString,
    Generic,
    Protocol,
    Type,
    TypeVar,
    runtime_checkable,
)

T = TypeVar("T")


class BAREType(Protocol, Generic[T]):
    @abstractmethod
    def pack(self, value: T) -> ByteString: ...

    @classmethod
    @abstractmethod
    def unpack(cls, fp: BinaryIO) -> T: ...

    @classmethod
    @abstractmethod
    def validate(cls, value: T) -> bool:
        return False

    @classmethod
    @abstractmethod
    def __eq__(cls, other: Any) -> bool:
        return False

    @classmethod
    @abstractmethod
    def __hash__(cls): ...
