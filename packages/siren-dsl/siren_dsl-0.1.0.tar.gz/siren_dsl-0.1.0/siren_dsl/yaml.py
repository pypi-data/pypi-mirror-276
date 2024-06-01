from __future__ import annotations
from abc import abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from typing import (Any, Protocol)
from .fable-library.list import (of_seq, FSharpList)
from .fable-library.option import (default_arg, value as value_1)
from .fable-library.reflection import (TypeInfo, int32_type, record_type, list_type, string_type, union_type)
from .fable-library.string_ import initialize
from .fable-library.system_text import (StringBuilder__ctor, StringBuilder__AppendLine_Z721C83C5)
from .fable-library.types import (Record, Array, Union, to_string)
from .fable-library.util import (get_enumerator, ignore)

def _expr0() -> TypeInfo:
    return record_type("Siren.Yaml.Config", [], Yaml_Config, lambda: [("Whitespace", int32_type), ("Level", int32_type)])


@dataclass(eq = False, repr = False, slots = True)
class Yaml_Config(Record):
    Whitespace: int
    Level: int

Yaml_Config_reflection = _expr0

def Yaml_Config_init_71136F3F(whitespace: int | None=None) -> Yaml_Config:
    return Yaml_Config(default_arg(whitespace, 4), 0)


def Yaml_Config__get_WhitespaceString(this: Yaml_Config) -> str:
    def _arrow1(_arg: int, this: Any=this) -> str:
        return " "

    return initialize(this.Level * this.Whitespace, _arrow1)


def _expr2() -> TypeInfo:
    return union_type("Siren.Yaml.AST", [], Yaml_AST, lambda: [[("Item", list_type(Yaml_AST_reflection()))], [("Item", list_type(Yaml_AST_reflection()))], [("Item", string_type)]])


class Yaml_AST(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Root", "Level", "Line"]


Yaml_AST_reflection = _expr2

def Yaml_AST_write_Z553CCAF4(root_element: Yaml_AST, fconfig: Callable[[Yaml_Config], Yaml_Config] | None=None) -> str:
    config_1: Yaml_Config
    config: Yaml_Config = Yaml_Config_init_71136F3F()
    config_1 = value_1(fconfig)(config) if (fconfig is not None) else config
    sb: Any = StringBuilder__ctor()
    def loop(current: Yaml_AST, sb_1: Any, config_2: Yaml_Config, root_element: Any=root_element, fconfig: Any=fconfig) -> None:
        if current.tag == 1:
            next_config: Yaml_Config = Yaml_Config(config_2.Whitespace, config_2.Level + 1)
            with get_enumerator(current.fields[0]) as enumerator:
                while enumerator.System_Collections_IEnumerator_MoveNext():
                    loop(enumerator.System_Collections_Generic_IEnumerator_1_get_Current(), sb_1, next_config)

        elif current.tag == 0:
            with get_enumerator(current.fields[0]) as enumerator_1:
                while enumerator_1.System_Collections_IEnumerator_MoveNext():
                    loop(enumerator_1.System_Collections_Generic_IEnumerator_1_get_Current(), sb_1, config_2)

        else: 
            ignore(StringBuilder__AppendLine_Z721C83C5(sb_1, Yaml_Config__get_WhitespaceString(config_2) + current.fields[0]))


    loop(root_element, sb, config_1)
    return to_string(sb)


def Yaml_line(line: str) -> Yaml_AST:
    return Yaml_AST(2, line)


def Yaml_level(children: Any | None=None) -> Yaml_AST:
    return Yaml_AST(1, of_seq(children))


def Yaml_root(children: Any | None=None) -> Yaml_AST:
    return Yaml_AST(0, of_seq(children))


def Yaml_write(root_element: Yaml_AST) -> str:
    return Yaml_AST_write_Z553CCAF4(root_element)


class IYamlConvertible(Protocol):
    @abstractmethod
    def ToYamlAst(self) -> FSharpList[Yaml_AST]:
        ...


__all__ = ["Yaml_Config_reflection", "Yaml_Config_init_71136F3F", "Yaml_Config__get_WhitespaceString", "Yaml_AST_reflection", "Yaml_AST_write_Z553CCAF4", "Yaml_line", "Yaml_level", "Yaml_root", "Yaml_write"]

