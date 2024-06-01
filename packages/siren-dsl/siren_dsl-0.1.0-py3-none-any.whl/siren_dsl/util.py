from collections.abc import Callable
from typing import TypeVar
from .fable-library.option import value

_A = TypeVar("_A")

_T = TypeVar("_T")

def Option_formatString(format: Callable[[str], str], str_1: str | None=None) -> str:
    if str_1 is not None:
        return format(str_1)

    else: 
        return ""



def Option_defaultBind(mapping: Callable[[_A], _T], def_: _T, opt: _A | None=None) -> _T:
    if opt is None:
        return def_

    else: 
        return mapping(value(opt))



def Bool_toString(b: bool) -> str:
    if b:
        return "true"

    else: 
        return "false"



__all__ = ["Option_formatString", "Option_defaultBind", "Bool_toString"]

