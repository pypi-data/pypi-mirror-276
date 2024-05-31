import io
from typing import Any, BinaryIO, Generic, Iterable, List, Optional, Self, Type, TypeVar

from .number import UInt

T = TypeVar("T")
A = List[T]


__all__ = ["Array", "array"]


class ArrayMeta(type):
    def __new__(
        cls,
        name,
        bases,
        namespace,
        *,
        inner: type | None = None,
        size: Optional[int] = None,
    ):
        inner_type = inner or namespace.get("_type", None)
        if inner_type is None and name != "Array":
            raise TypeError("Array must have an inner type")
        namespace["_type"] = inner_type
        if size is None and name != "Array":
            size = namespace.get("_size", None)
        namespace["_size"] = size
        return super().__new__(cls, name, bases, namespace)


class ArrayValidator(Generic[T]):
    def __init__(self, ty: Type[A]):
        self.ty = ty

    def __get__(self, inst, _) -> list[T] | Type[T]:
        if inst is None:
            return self.ty
        return inst.__dict__["_inner"]

    def __set__(self, inst, value: Iterable[T]):
        v = []
        for v in value:
            if not self.ty.validate(v):
                raise TypeError(
                    f"type {type(value)} is invalid for field of BARE type {self.ty}"
                )
            if not isinstance(v, self.ty):
                v.append(self.ty(v))
            else:
                v.append(v)
        inst.__dict__["_inner"] = v


class Array(Generic[T], metaclass=ArrayMeta):
    """
    A BARE array type. It's inner type must be a BARE type defined in this package and
    must be supplied as a metaclass argument to a subclass of the `Array` class using
    the `inner` kwarg.

    A `size` kwarg may also be specified, which will make the new subclass a fixed-size
    array, which does not encode the length of the array in the serialized data.

    An example that uses both of these:

        class MyArray(Array, inner=UInt, size=10):
            ...

    You do *not* need to specify any fields or methods on the subclass, though you may.
    The above class `MyArray` is a fixed size array of 10 `UInt` values.
    """

    value: list[A]
    _type: Type[T]
    _size: int | None

    def __init__(self, value: Iterable[A]):
        self.value = ArrayValidator(self.__class__._type)
        inner = []
        for v in value:
            if not isinstance(v, self.__class__._type):
                v = self.__class__._type(v)
            else:
                v = v
            inner.append(v)
        self.value = inner

    def __getitem__(self, key):
        return self.value[key]

    def __iter__(self):
        return iter(self.value)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Array):
            return other.value == self.value
        try:
            values = list(iter(other))
            for other_value, self_value in zip(values, self.value):
                if other_value != self_value:
                    return False
            return True
        except TypeError:
            pass
        return NotImplemented

    def pack(self) -> bytes:
        fp = io.BytesIO()
        if self._size is None:
            fp.write(UInt(len(self.value)).pack())

        for item in self.value:
            fp.write(item.pack())
        return fp.getbuffer()

    @classmethod
    def unpack(cls, fp: BinaryIO) -> Self:
        size = cls._size or UInt.unpack(fp).value
        out = []
        for _ in range(size):
            out.append(cls._type.unpack(fp))
        return cls(out)

    @classmethod
    def validate(cls, value: Iterable[T]) -> bool:
        value = list(value)
        if cls._size:
            if len(value) != cls._size:
                return False
        for v in value:
            if not cls._type.validate(v):
                return False
        return True


def array(inner: type, size: Optional[int] = None) -> Type[Array[A]]:
    """
    A function that defines and returns anonymous BARE `Array` subclass with
    the provided `inner` type and (optional) `size` arguments.


    Proper usage of this function is as follows:

        MyArray = array(UInt, size=10)

    Note that the name of the class is unspecified, use at your own risk.
    """
    size_name = f"_size_{size}" if size else ""
    name = f"Array_{inner.__name__}{size_name}_anonymous"
    namespace = ArrayMeta.__prepare__(name, (Array,), inner=inner, size=size)
    AnonymousArray = ArrayMeta.__new__(
        ArrayMeta, name, (Array,), namespace, inner=inner, size=size
    )
    ArrayMeta.__init__(AnonymousArray, name, (Array,), namespace)  # type: ignore
    return AnonymousArray
