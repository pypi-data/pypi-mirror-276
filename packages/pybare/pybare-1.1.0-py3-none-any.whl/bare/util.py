from typing import Generic, Type

from .baretype import BAREType, T


class ValidationError(TypeError):
    def __init__(expected: type, actual: type):
        super().__init__(
            f"Got invalid type. Expected {expected.__name__}, got {actual.__name__}"
        )


class Field(Generic[T]):
    """
    A descriptor that assists with assigning/retrieving values from a BARE Struct.
    It is reponsible for performing type validation on assignment of struct fields.

    For example:
        class MyStruct(Struct):
            a = Field(UInt)
            b = Field(Str)
    """

    attr: str
    name: str
    ty: Type[T]

    def __init__(self, ty: Type[T], attr: str | None = None):
        # ignore the typing here because these will always be set when assigned to an
        # object
        self.attr = attr  # type: ignore
        self.ty = ty

    def __get__(self, inst, _) -> T | Type[T]:
        if inst is None:
            return self.ty
        return inst.__dict__[self.attr]

    def __set__(self, inst, value: T):
        if not isinstance(value, self.ty) and not self.ty.validate(value):
            raise TypeError(
                f"type {type(value)} is invalid for field of BARE type {self.ty}"
            )
        inst.__dict__[self.attr] = value
