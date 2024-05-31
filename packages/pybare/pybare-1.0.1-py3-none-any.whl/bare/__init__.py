"""
pybare is a Python library for writing and reading binary data using the BARE
serialization format.
"""

from .barearray import Array, array
from .barestruct import Field, Struct
from .data import Data, data
from .map import Map, map
from .misc import Enum, Str, Void
from .number import F32, F64, I8, I16, I32, I64, U8, U16, U32, U64, Bool, Int, UInt
from .union import Union, UnionVariant, optional, union

__all__ = [
    "F32",
    "F64",
    "I8",
    "I16",
    "I32",
    "I64",
    "U8",
    "Bool",
    "U16",
    "U32",
    "U64",
    "Int",
    "UInt",
    "Data",
    "data",
    "Union",
    "UnionVariant",
    "optional",
    "union",
    "Enum",
    "Str",
    "Void",
    "Array",
    "array",
    "Field",
    "Struct",
    "Map",
    "map",
]
