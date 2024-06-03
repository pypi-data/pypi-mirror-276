from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from .fable-library.list import (map as map_1, FSharpList, filter, of_array, choose, of_seq)
from .fable-library.option import (default_arg, map, value as value_1)
from .fable-library.seq import (map as map_2, to_list, delay, append, singleton, is_empty, collect)
from .fable-library.seq2 import distinct
from .fable-library.string_ import (to_text, printf, join, to_fail, initialize, replace, trim_end)
from .fable-library.types import to_string as to_string_1
from .fable-library.util import (int32_to_string, equals, structural_hash, IEnumerable_1)
from .siren_types import (NotePosition, Direction, FlowchartLinkTypes, FlowchartNodeTypes, SequenceMessageTypes, ClassMemberVisibility, ClassMemberClassifier, ClassRelationshipDirection, ClassRelationshipType, ClassCardinality, ERCardinalityType, ERKeyType, ERAttribute, GanttTags, GanttUnit, RDRiskType, RDVerifyMethod, RDRelationship, RequirementDiagramElement, GitCommitType, MindmapShape, MindmapElement, TimelineElement, SankeyElement, BlockBlockType, BlockArrowDirection)
from .util import Option_formatString

__B = TypeVar("__B")

def Siren_NotePosition__NotePosition_ToFormatString(this: NotePosition) -> str:
    if this.tag == 1:
        return "right of"

    elif this.tag == 2:
        return "left of"

    else: 
        return "over"



def Generic_formatComment(txt: str) -> str:
    return to_text(printf("%%%% %s"))(txt)


def Generic_formatDirection(direction: Direction) -> str:
    arg: str = to_string_1(direction)
    return to_text(printf("direction %s"))(arg)


def Generic_formatClickHref(id: str, url: str, tooltip: str | None=None) -> str:
    def mapping(s: str, id: Any=id, url: Any=url, tooltip: Any=tooltip) -> str:
        return to_text(printf(" \"%s\""))(s)

    tooltip_1: str = default_arg(map(mapping, tooltip), "")
    return to_text(printf("click %s href \"%s\"%s"))(id)(url)(tooltip_1)


def Generic_formatNote(id: str, position: NotePosition | None, msg: str) -> str:
    position_1: str = Siren_NotePosition__NotePosition_ToFormatString(default_arg(position, NotePosition(1)))
    return to_text(printf("note %s %s : %s"))(position_1)(id)(msg)


def Generic_formatClassDef(class_name: str, styles0: FSharpList[tuple[str, str]]) -> str:
    def mapping(tupled_arg: tuple[str, str], class_name: Any=class_name, styles0: Any=styles0) -> str:
        return to_text(printf("%s:%s"))(tupled_arg[0])(tupled_arg[1])

    styles: str = join(",", map_1(mapping, styles0))
    return to_text(printf("classDef %s %s;"))(class_name)(styles)


def Generic_formatClass(node_ids0: FSharpList[str], class_name: str) -> str:
    ids: str = join(",", node_ids0)
    return to_text(printf("class %s %s;"))(ids)(class_name)


def Siren_FlowchartLinkTypes__FlowchartLinkTypes_appendTextOption_Static(txt: str | None, arrow: str) -> str:
    if txt is not None:
        arg_1: str = value_1(txt)
        return to_text(printf("%s|%s|"))(arrow)(arg_1)

    else: 
        return arrow



def Siren_FlowchartLinkTypes__FlowchartLinkTypes_AddedLengthLinker_71136F3F(this: FlowchartLinkTypes, added_length: int | None=None) -> str:
    added_length_1: int = default_arg(added_length, 1) or 0
    if added_length_1 < 1:
        to_fail(printf("Minimum length of a link was set below 1: %i"))(added_length_1)

    char: str = Siren_FlowchartLinkTypes__FlowchartLinkTypes_GetAddLengthChar(this)
    def _arrow89(i: int, this: Any=this, added_length: Any=added_length) -> str:
        return char

    return initialize(added_length_1, _arrow89)


def Siren_FlowchartLinkTypes__FlowchartLinkTypes_GetAddLengthChar(this: FlowchartLinkTypes) -> str:
    if (((((this.tag == 0) or (this.tag == 7)) or (this.tag == 8)) or (this.tag == 9)) or (this.tag == 10)) or (this.tag == 11):
        return "-"

    elif (this.tag == 2) or (this.tag == 3):
        return "."

    elif (this.tag == 4) or (this.tag == 5):
        return "="

    elif this.tag == 6:
        return "~"

    else: 
        return "-"



def Flowchart_formatMinimalNamedNode(id: str, name: str) -> str:
    return ((("" + id) + "[") + name) + "]"


def Flowchart_nodeTypeToFormatter(nodetype: FlowchartNodeTypes) -> Callable[[str, str], str]:
    if nodetype.tag == 1:
        def _arrow91(id_1: str, nodetype: Any=nodetype) -> Callable[[str], str]:
            def _arrow90(name_1: str) -> str:
                return ((("" + id_1) + "(") + name_1) + ")"

            return _arrow90

        return _arrow91

    elif nodetype.tag == 2:
        def _arrow93(id_2: str, nodetype: Any=nodetype) -> Callable[[str], str]:
            def _arrow92(name_2: str) -> str:
                return ((("" + id_2) + "([") + name_2) + "])"

            return _arrow92

        return _arrow93

    elif nodetype.tag == 3:
        def _arrow95(id_3: str, nodetype: Any=nodetype) -> Callable[[str], str]:
            def _arrow94(name_3: str) -> str:
                return ((("" + id_3) + "[[") + name_3) + "]]"

            return _arrow94

        return _arrow95

    elif nodetype.tag == 4:
        def _arrow97(id_4: str, nodetype: Any=nodetype) -> Callable[[str], str]:
            def _arrow96(name_4: str) -> str:
                return ((("" + id_4) + "[(") + name_4) + ")]"

            return _arrow96

        return _arrow97

    elif nodetype.tag == 5:
        def _arrow99(id_5: str, nodetype: Any=nodetype) -> Callable[[str], str]:
            def _arrow98(name_5: str) -> str:
                return ((("" + id_5) + "((") + name_5) + "))"

            return _arrow98

        return _arrow99

    elif nodetype.tag == 6:
        def _arrow101(id_6: str, nodetype: Any=nodetype) -> Callable[[str], str]:
            def _arrow100(name_6: str) -> str:
                return ((("" + id_6) + ">") + name_6) + "]"

            return _arrow100

        return _arrow101

    elif nodetype.tag == 7:
        def _arrow103(id_7: str, nodetype: Any=nodetype) -> Callable[[str], str]:
            def _arrow102(name_7: str) -> str:
                return to_text(printf("%s{%s}"))(id_7)(name_7)

            return _arrow102

        return _arrow103

    elif nodetype.tag == 8:
        def _arrow105(id_8: str, nodetype: Any=nodetype) -> Callable[[str], str]:
            def _arrow104(name_8: str) -> str:
                return to_text(printf("%s{{%s}}"))(id_8)(name_8)

            return _arrow104

        return _arrow105

    elif nodetype.tag == 9:
        def _arrow107(id_9: str, nodetype: Any=nodetype) -> Callable[[str], str]:
            def _arrow106(name_9: str) -> str:
                return to_text(printf("%s[/%s/]"))(id_9)(name_9)

            return _arrow106

        return _arrow107

    elif nodetype.tag == 10:
        def _arrow109(id_10: str, nodetype: Any=nodetype) -> Callable[[str], str]:
            def _arrow108(name_10: str) -> str:
                return to_text(printf("%s[\\%s\\]"))(id_10)(name_10)

            return _arrow108

        return _arrow109

    elif nodetype.tag == 11:
        def _arrow111(id_11: str, nodetype: Any=nodetype) -> Callable[[str], str]:
            def _arrow110(name_11: str) -> str:
                return to_text(printf("%s[/%s\\]"))(id_11)(name_11)

            return _arrow110

        return _arrow111

    elif nodetype.tag == 12:
        def _arrow113(id_12: str, nodetype: Any=nodetype) -> Callable[[str], str]:
            def _arrow112(name_12: str) -> str:
                return to_text(printf("%s[\\%s/]"))(id_12)(name_12)

            return _arrow112

        return _arrow113

    elif nodetype.tag == 13:
        def _arrow115(id_13: str, nodetype: Any=nodetype) -> Callable[[str], str]:
            def _arrow114(name_13: str) -> str:
                return to_text(printf("%s(((%s)))"))(id_13)(name_13)

            return _arrow114

        return _arrow115

    else: 
        def _arrow117(id: str, nodetype: Any=nodetype) -> Callable[[str], str]:
            def _arrow116(name: str) -> str:
                return Flowchart_formatMinimalNamedNode(id, name)

            return _arrow116

        return _arrow117



def Flowchart_formatNode(id: str, name: str | None, shape: FlowchartNodeTypes) -> str:
    return Flowchart_nodeTypeToFormatter(shape)(id)(default_arg(name, id))


def Flowchart_formatLinkType(link: FlowchartLinkTypes, msg: str | None=None, added_length: int | None=None) -> str:
    return Siren_FlowchartLinkTypes__FlowchartLinkTypes_appendTextOption_Static(msg, (("-" + Siren_FlowchartLinkTypes__FlowchartLinkTypes_AddedLengthLinker_71136F3F(link, added_length)) + "-") if (link.tag == 1) else ((("-" + Siren_FlowchartLinkTypes__FlowchartLinkTypes_AddedLengthLinker_71136F3F(link, added_length)) + "-") if (link.tag == 2) else ((("-" + Siren_FlowchartLinkTypes__FlowchartLinkTypes_AddedLengthLinker_71136F3F(link, added_length)) + "->") if (link.tag == 3) else ((("=" + Siren_FlowchartLinkTypes__FlowchartLinkTypes_AddedLengthLinker_71136F3F(link, added_length)) + "=") if (link.tag == 4) else ((("=" + Siren_FlowchartLinkTypes__FlowchartLinkTypes_AddedLengthLinker_71136F3F(link, added_length)) + ">") if (link.tag == 5) else ((("~" + Siren_FlowchartLinkTypes__FlowchartLinkTypes_AddedLengthLinker_71136F3F(link, added_length)) + "~") if (link.tag == 6) else ((("-" + Siren_FlowchartLinkTypes__FlowchartLinkTypes_AddedLengthLinker_71136F3F(link, added_length)) + "o") if (link.tag == 7) else ((("-" + Siren_FlowchartLinkTypes__FlowchartLinkTypes_AddedLengthLinker_71136F3F(link, added_length)) + "x") if (link.tag == 8) else ((("<-" + Siren_FlowchartLinkTypes__FlowchartLinkTypes_AddedLengthLinker_71136F3F(link, added_length)) + ">") if (link.tag == 9) else ((("o-" + Siren_FlowchartLinkTypes__FlowchartLinkTypes_AddedLengthLinker_71136F3F(link, added_length)) + "o") if (link.tag == 10) else ((("x-" + Siren_FlowchartLinkTypes__FlowchartLinkTypes_AddedLengthLinker_71136F3F(link, added_length)) + "x") if (link.tag == 11) else (("-" + Siren_FlowchartLinkTypes__FlowchartLinkTypes_AddedLengthLinker_71136F3F(link, added_length)) + ">"))))))))))))


def Flowchart_formatLink(n1: str, n2: str, link: FlowchartLinkTypes, msg: str | None=None, added_length: int | None=None) -> str:
    return (n1 + Flowchart_formatLinkType(link, msg, added_length)) + n2


def Flowchart_formatSubgraph(id: str, name: str | None=None) -> str:
    name_str: str
    if name is not None:
        arg: str = value_1(name)
        name_str = to_text(printf("[%s]"))(arg)

    else: 
        name_str = ""

    return to_text(printf("subgraph %s%s"))(id)(name_str)


def Flowchart_formatLinkStyles(ids0: FSharpList[int], styles0: FSharpList[tuple[str, str]]) -> str:
    def mapping(tupled_arg: tuple[str, str], ids0: Any=ids0, styles0: Any=styles0) -> str:
        return to_text(printf("%s:%s"))(tupled_arg[0])(tupled_arg[1])

    styles: str = join(",", map_1(mapping, styles0))
    def mapping_1(value: int, ids0: Any=ids0, styles0: Any=styles0) -> str:
        return int32_to_string(value)

    ids: str = join(",", map_1(mapping_1, ids0))
    return to_text(printf("linkStyle %s %s;"))(ids)(styles)


def Flowchart_formatNodeStyles(ids0: FSharpList[str], styles0: FSharpList[tuple[str, str]]) -> str:
    def mapping(tupled_arg: tuple[str, str], ids0: Any=ids0, styles0: Any=styles0) -> str:
        return to_text(printf("%s:%s"))(tupled_arg[0])(tupled_arg[1])

    styles: str = join(",", map_1(mapping, styles0))
    ids: str = join(",", ids0)
    return to_text(printf("style %s %s;"))(ids)(styles)


def Sequence_formatMessageType(msg_type: SequenceMessageTypes) -> str:
    if msg_type.tag == 1:
        return "-->"

    elif msg_type.tag == 2:
        return "->>"

    elif msg_type.tag == 3:
        return "-->>"

    elif msg_type.tag == 4:
        return "-x"

    elif msg_type.tag == 5:
        return "--x"

    elif msg_type.tag == 6:
        return "-)"

    elif msg_type.tag == 7:
        return "--)"

    else: 
        return "->"



def Sequence_formatMessage(a1: str, a2: str, msg_type: SequenceMessageTypes, msg: str, activate: bool | None=None) -> str:
    active: str = ("+" if activate else "-") if (activate is not None) else ""
    arg_1: str = Sequence_formatMessageType(msg_type)
    return to_text(printf("%s%s%s%s: %s"))(a1)(arg_1)(active)(a2)(msg)


def Sequence_formatParticipant(name: str, alias: str | None=None) -> str:
    def format(s: str, name: Any=name, alias: Any=alias) -> str:
        return to_text(printf(" as %s"))(s)

    alias_1: str = Option_formatString(format, alias)
    return to_text(printf("participant %s%s"))(name)(alias_1)


def Sequence_formatActor(name: str, alias: str | None=None) -> str:
    def format(s: str, name: Any=name, alias: Any=alias) -> str:
        return to_text(printf(" as %s"))(s)

    alias_1: str = Option_formatString(format, alias)
    return to_text(printf("actor %s%s"))(name)(alias_1)


def Sequence_formatCreate(formatter: Callable[[str, str | None], str], name: str, alias: str | None=None) -> str:
    arg: str = formatter(name, alias)
    return to_text(printf("create %s"))(arg)


def Sequence_formatDestroy(id: str) -> str:
    return to_text(printf("destroy %s"))(id)


def Sequence_formatBox(name: str, color: str | None=None) -> str:
    def _arrow118(__unit: None=None, name: Any=name, color: Any=color) -> Callable[[str], str]:
        clo: Callable[[str], str] = to_text(printf("%s "))
        return clo

    color_1: str = Option_formatString(_arrow118(), color)
    return to_text(printf("box %s%s"))(color_1)(name)


def Sequence_formatNoteSpanning(id1: str, id2: str, position: NotePosition | None, msg: str) -> str:
    position_1: str = Siren_NotePosition__NotePosition_ToFormatString(default_arg(position, NotePosition(1)))
    return to_text(printf("note %s %s,%s : %s"))(position_1)(id1)(id2)(msg)


def Siren_ClassMemberVisibility__ClassMemberVisibility_ToFormatString(this: ClassMemberVisibility) -> str:
    if this.tag == 1:
        return "-"

    elif this.tag == 2:
        return "#"

    elif this.tag == 3:
        return "~"

    elif this.tag == 4:
        return this.fields[0]

    else: 
        return "+"



def Siren_ClassMemberClassifier__ClassMemberClassifier_ToFormatString(this: ClassMemberClassifier) -> str:
    if this.tag == 1:
        return "$"

    elif this.tag == 2:
        return this.fields[0]

    else: 
        return "*"



def Siren_ClassRelationshipDirection__ClassRelationshipDirection_ToFormatString_30230F9B(this: ClassRelationshipDirection, left: str, right: str, center: str) -> str:
    if this.tag == 1:
        return center + right

    elif this.tag == 2:
        return (left + center) + right

    else: 
        return left + center



def Siren_ClassRelationshipDirection__ClassRelationshipDirection_ToFormatString_Z384F8060(this: ClassRelationshipDirection, edge: str, center: str) -> str:
    if this.tag == 1:
        return center + edge

    elif this.tag == 2:
        return (edge + center) + edge

    else: 
        return edge + center



def Siren_ClassRelationshipType__ClassRelationshipType_ToFormatString_7464358D(this: ClassRelationshipType, direction: ClassRelationshipDirection | None=None, is_dotted: bool | None=None) -> str:
    center: str = ".." if default_arg(is_dotted, False) else "--"
    direct: ClassRelationshipDirection = default_arg(direction, ClassRelationshipDirection(1))
    if this.tag == 1:
        return Siren_ClassRelationshipDirection__ClassRelationshipDirection_ToFormatString_Z384F8060(direct, "*", center)

    elif this.tag == 2:
        return Siren_ClassRelationshipDirection__ClassRelationshipDirection_ToFormatString_Z384F8060(direct, "o", center)

    elif this.tag == 3:
        return Siren_ClassRelationshipDirection__ClassRelationshipDirection_ToFormatString_30230F9B(direct, "<", ">", center)

    elif this.tag == 4:
        return center

    elif this.tag == 5:
        return "--"

    elif this.tag == 6:
        return ".."

    elif this.tag == 7:
        return Siren_ClassRelationshipDirection__ClassRelationshipDirection_ToFormatString_30230F9B(direct, "<", ">", "..")

    elif this.tag == 8:
        return Siren_ClassRelationshipDirection__ClassRelationshipDirection_ToFormatString_30230F9B(direct, "<|", "|>", "..")

    else: 
        return Siren_ClassRelationshipDirection__ClassRelationshipDirection_ToFormatString_30230F9B(direct, "<|", "|>", center)



def Siren_ClassCardinality__ClassCardinality_ToFormatString(this: ClassCardinality) -> str:
    if this.tag == 1:
        return "0..1"

    elif this.tag == 2:
        return "1..*"

    elif this.tag == 3:
        return "*"

    elif this.tag == 4:
        return "n"

    elif this.tag == 5:
        return "0..n"

    elif this.tag == 6:
        return "1..n"

    elif this.tag == 7:
        return this.fields[0]

    else: 
        return "1"



def ClassDiagram_formatClass(id: str, name: str | None=None, generic: str | None=None) -> str:
    def format(s: str, id: Any=id, name: Any=name, generic: Any=generic) -> str:
        return to_text(printf("[\"%s\"]"))(s)

    name_1: str = Option_formatString(format, name)
    def format_1(s_1: str, id: Any=id, name: Any=name, generic: Any=generic) -> str:
        return to_text(printf("~%s~"))(s_1)

    generic_1: str = Option_formatString(format_1, generic)
    return to_text(printf("class %s%s%s"))(id)(generic_1)(name_1)


def ClassDiagram_formatClassMember(name: str, visibility: ClassMemberVisibility | None=None, classifier: ClassMemberClassifier | None=None) -> str:
    def format(x: str, name: Any=name, visibility: Any=visibility, classifier: Any=classifier) -> str:
        return x

    def mapping(_arg: ClassMemberVisibility, name: Any=name, visibility: Any=visibility, classifier: Any=classifier) -> str:
        return Siren_ClassMemberVisibility__ClassMemberVisibility_ToFormatString(_arg)

    def format_1(x_1: str, name: Any=name, visibility: Any=visibility, classifier: Any=classifier) -> str:
        return x_1

    def mapping_1(_arg_1: ClassMemberClassifier, name: Any=name, visibility: Any=visibility, classifier: Any=classifier) -> str:
        return Siren_ClassMemberClassifier__ClassMemberClassifier_ToFormatString(_arg_1)

    return (Option_formatString(format, map(mapping, visibility)) + name) + Option_formatString(format_1, map(mapping_1, classifier))


def ClassDiagram_formatGeneric(generic: str) -> str:
    return replace(replace(generic, "<", "~"), ">", "~")


def ClassDiagram_formatClassAttr(name: str, generic: str | None=None, visibility: ClassMemberVisibility | None=None, classifier: ClassMemberClassifier | None=None) -> str:
    def _arrow120(generic_1: str, name: Any=name, generic: Any=generic, visibility: Any=visibility, classifier: Any=classifier) -> str:
        return ClassDiagram_formatGeneric(generic_1)

    generic_2: str = Option_formatString(_arrow120, generic)
    def format(x: str, name: Any=name, generic: Any=generic, visibility: Any=visibility, classifier: Any=classifier) -> str:
        return x

    def mapping(_arg: ClassMemberVisibility, name: Any=name, generic: Any=generic, visibility: Any=visibility, classifier: Any=classifier) -> str:
        return Siren_ClassMemberVisibility__ClassMemberVisibility_ToFormatString(_arg)

    visibility_1: str = Option_formatString(format, map(mapping, visibility))
    def format_1(x_1: str, name: Any=name, generic: Any=generic, visibility: Any=visibility, classifier: Any=classifier) -> str:
        return x_1

    def mapping_1(_arg_1: ClassMemberClassifier, name: Any=name, generic: Any=generic, visibility: Any=visibility, classifier: Any=classifier) -> str:
        return Siren_ClassMemberClassifier__ClassMemberClassifier_ToFormatString(_arg_1)

    classifier_1: str = Option_formatString(format_1, map(mapping_1, classifier))
    _arg_2: str = to_text(printf("%s%s %s%s"))(visibility_1)(generic_2)(name)(classifier_1)
    return _arg_2.strip()


def ClassDiagram_formatClassFunction(name: str, args: str | None=None, return_type: str | None=None, visibility: ClassMemberVisibility | None=None, classifier: ClassMemberClassifier | None=None) -> str:
    def format(x: str, name: Any=name, args: Any=args, return_type: Any=return_type, visibility: Any=visibility, classifier: Any=classifier) -> str:
        return x

    def mapping(_arg: ClassMemberVisibility, name: Any=name, args: Any=args, return_type: Any=return_type, visibility: Any=visibility, classifier: Any=classifier) -> str:
        return Siren_ClassMemberVisibility__ClassMemberVisibility_ToFormatString(_arg)

    visibility_1: str = Option_formatString(format, map(mapping, visibility))
    def format_1(x_1: str, name: Any=name, args: Any=args, return_type: Any=return_type, visibility: Any=visibility, classifier: Any=classifier) -> str:
        return x_1

    def mapping_1(_arg_1: ClassMemberClassifier, name: Any=name, args: Any=args, return_type: Any=return_type, visibility: Any=visibility, classifier: Any=classifier) -> str:
        return Siren_ClassMemberClassifier__ClassMemberClassifier_ToFormatString(_arg_1)

    classifier_1: str = Option_formatString(format_1, map(mapping_1, classifier))
    args_1: str = ClassDiagram_formatGeneric(default_arg(args, ""))
    def format_2(x_2: str, name: Any=name, args: Any=args, return_type: Any=return_type, visibility: Any=visibility, classifier: Any=classifier) -> str:
        arg: str = ClassDiagram_formatGeneric(x_2)
        return to_text(printf(" %s"))(arg)

    return_type_1: str = Option_formatString(format_2, return_type)
    return to_text(printf("%s%s(%s)%s%s"))(visibility_1)(name)(args_1)(return_type_1)(classifier_1)


def ClassDiagram_formatMember(id: str, label: str, visibility: ClassMemberVisibility | None=None, classifier: ClassMemberClassifier | None=None) -> str:
    arg_1: str = ClassDiagram_formatClassMember(label, visibility, classifier)
    return to_text(printf("%s : %s"))(id)(arg_1)


def ClassDiagram_formatAttr(id: str, name: str, generic: str | None=None, visibility: ClassMemberVisibility | None=None, classifier: ClassMemberClassifier | None=None) -> str:
    arg_1: str = ClassDiagram_formatClassAttr(name, generic, visibility, classifier)
    return to_text(printf("%s : %s"))(id)(arg_1)


def ClassDiagram_formatFunction(id: str, name: str, args: str | None=None, return_type: str | None=None, visibility: ClassMemberVisibility | None=None, classifier: ClassMemberClassifier | None=None) -> str:
    arg_1: str = ClassDiagram_formatClassFunction(name, args, return_type, visibility, classifier)
    return to_text(printf("%s : %s"))(id)(arg_1)


def ClassDiagram_formatRelationship0(id1: str, id2: str, link: str, label: str | None=None, cardinality1: ClassCardinality | None=None, cardinality2: ClassCardinality | None=None) -> str:
    def format(s: str, id1: Any=id1, id2: Any=id2, link: Any=link, label: Any=label, cardinality1: Any=cardinality1, cardinality2: Any=cardinality2) -> str:
        return to_text(printf(" \"%s\""))(s)

    def mapping(_arg: ClassCardinality, id1: Any=id1, id2: Any=id2, link: Any=link, label: Any=label, cardinality1: Any=cardinality1, cardinality2: Any=cardinality2) -> str:
        return Siren_ClassCardinality__ClassCardinality_ToFormatString(_arg)

    car1: str = Option_formatString(format, map(mapping, cardinality1))
    def format_1(s_1: str, id1: Any=id1, id2: Any=id2, link: Any=link, label: Any=label, cardinality1: Any=cardinality1, cardinality2: Any=cardinality2) -> str:
        return to_text(printf("\"%s\" "))(s_1)

    def mapping_1(_arg_1: ClassCardinality, id1: Any=id1, id2: Any=id2, link: Any=link, label: Any=label, cardinality1: Any=cardinality1, cardinality2: Any=cardinality2) -> str:
        return Siren_ClassCardinality__ClassCardinality_ToFormatString(_arg_1)

    car2: str = Option_formatString(format_1, map(mapping_1, cardinality2))
    def format_2(l: str, id1: Any=id1, id2: Any=id2, link: Any=link, label: Any=label, cardinality1: Any=cardinality1, cardinality2: Any=cardinality2) -> str:
        return to_text(printf(" : %s"))(l)

    label_1: str = Option_formatString(format_2, label)
    return to_text(printf("%s%s %s %s%s%s"))(id1)(car1)(link)(car2)(id2)(label_1)


def ClassDiagram_formatRelationship(id1: str, id2: str, rlts_type: ClassRelationshipType, label: str | None=None, cardinality1: ClassCardinality | None=None, cardinality2: ClassCardinality | None=None) -> str:
    return ClassDiagram_formatRelationship0(id1, id2, Siren_ClassRelationshipType__ClassRelationshipType_ToFormatString_7464358D(rlts_type, None, None), label, cardinality1, cardinality2)


def ClassDiagram_formatRelationshipCustom(id1: str, id2: str, rlts_type: ClassRelationshipType, direction: ClassRelationshipDirection | None=None, dotted: bool | None=None, label: str | None=None, cardinality1: ClassCardinality | None=None, cardinality2: ClassCardinality | None=None) -> str:
    return ClassDiagram_formatRelationship0(id1, id2, Siren_ClassRelationshipType__ClassRelationshipType_ToFormatString_7464358D(rlts_type, direction, dotted), label, cardinality1, cardinality2)


def ClassDiagram_formatAnnotation(id0: str | None, annotation: str) -> str:
    if id0 is None:
        return to_text(printf("<<%s>>"))(annotation)

    else: 
        id: str = id0
        return to_text(printf("<<%s>> %s"))(annotation)(id)



def ClassDiagram_formatNote(txt: str, id: str | None=None) -> str:
    if id is not None:
        arg: str = value_1(id)
        return to_text(printf("note for %s \"%s\""))(arg)(txt)

    else: 
        return to_text(printf("note \"%s\""))(txt)



def ClassDiagram_formatClassStyles(id: str, styles0: FSharpList[tuple[str, str]]) -> str:
    def mapping(tupled_arg: tuple[str, str], id: Any=id, styles0: Any=styles0) -> str:
        return to_text(printf("%s: %s"))(tupled_arg[0])(tupled_arg[1])

    styles: str = join(",", map_1(mapping, styles0))
    return to_text(printf("style %s %s"))(id)(styles)


def ClassDiagram_formatCssClass(ids0: FSharpList[str], class_name: str) -> str:
    ids: str = join(",", ids0)
    return to_text(printf("style \"%s\" %s;"))(ids)(class_name)


def StateDiagram_formatState(id: str, description: str | None=None) -> str:
    def format(s: str, id: Any=id, description: Any=description) -> str:
        return to_text(printf(" : %s"))(s)

    description_1: str = Option_formatString(format, description)
    return to_text(printf("%s%s"))(id)(description_1)


def StateDiagram_formatTransition(id1: str, id2: str, description: str | None=None) -> str:
    def format(s: str, id1: Any=id1, id2: Any=id2, description: Any=description) -> str:
        return to_text(printf(" : %s"))(s)

    description_1: str = Option_formatString(format, description)
    return to_text(printf("%s --> %s%s"))(id1)(id2)(description_1)


def StateDiagram_formatNoteWrapper(id: str, position: NotePosition | None=None) -> str:
    position_1: str = Siren_NotePosition__NotePosition_ToFormatString(default_arg(position, NotePosition(1)))
    return to_text(printf("note %s %s"))(position_1)(id)


def Siren_ERCardinalityType__ERCardinalityType_ToFormatString(this: ERCardinalityType) -> str:
    if this.tag == 1:
        return "one or many"

    elif this.tag == 2:
        return "zero or many"

    elif this.tag == 3:
        return "only one"

    else: 
        return "one or zero"



def ERDiagram_formatEntityNode(id: str, alias: str | None=None) -> str:
    def format(s: str, id: Any=id, alias: Any=alias) -> str:
        return to_text(printf("[\"%s\"]"))(s)

    alias_1: str = Option_formatString(format, alias)
    return to_text(printf("%s%s"))(id)(alias_1)


def ERDiagram_formatEntityWrapper(id: str, alias: str | None=None) -> str:
    return ERDiagram_formatEntityNode(id, alias) + " {"


def ERDiagram_formatAttribute(attr: ERAttribute) -> str:
    def predicate(s_1: str, attr: Any=attr) -> bool:
        return s_1 != ""

    def mapping(_arg: ERKeyType, attr: Any=attr) -> str:
        return to_string_1(_arg)

    def format(s: str, attr: Any=attr) -> str:
        return to_text(printf("\"%s\""))(s)

    return join(" ", filter(predicate, of_array([attr.Type, attr.Name, join(", ", map_1(mapping, attr.Keys)), Option_formatString(format, attr.Comment)])))


def ERDiagram_formatRelationship(id1: str, card1: ERCardinalityType, id2: str, card2: ERCardinalityType, msg: str, is_optional: bool | None=None) -> str:
    to_string: str = "optionally to" if default_arg(is_optional, False) else "to"
    arg_1: str = Siren_ERCardinalityType__ERCardinalityType_ToFormatString(card1)
    arg_3: str = Siren_ERCardinalityType__ERCardinalityType_ToFormatString(card2)
    return to_text(printf("%s %s %s %s %s : %s"))(id1)(arg_1)(to_string)(arg_3)(id2)(msg)


def UserJourney_formatTask(name: str, score: Any, actors: Any | None=None) -> str:
    def mapping(strings: __B | None=None, name: Any=name, score: Any=score, actors: Any=actors) -> str:
        return join(", ", strings)

    actors_1: str | None = map(mapping, actors)
    def _arrow125(x: str | None=None, name: Any=name, score: Any=score, actors: Any=actors) -> str | None:
        return x

    return join(": ", choose(_arrow125, of_array([name, to_string_1(score), actors_1])))


def Siren_GanttTags__GanttTags_ToFormatString(this: GanttTags) -> str:
    if this.tag == 1:
        return "done"

    elif this.tag == 2:
        return "crit"

    elif this.tag == 3:
        return "milestone"

    else: 
        return "active"



def Siren_GanttUnit__GanttUnit_ToFormatString(this: GanttUnit) -> str:
    _arg: str = to_string_1(this)
    return _arg.lower()


def Gantt_formatTask(title: str, tags: FSharpList[GanttTags], selfid: str | None=None, start_date: str | None=None, end_date: str | None=None) -> str:
    def mapping(x: GanttTags, title: Any=title, tags: Any=tags, selfid: Any=selfid, start_date: Any=start_date, end_date: Any=end_date) -> str | None:
        return Siren_GanttTags__GanttTags_ToFormatString(x)

    class ObjectExpr127:
        @property
        def Equals(self) -> Callable[[str | None, str | None], bool]:
            return equals

        @property
        def GetHashCode(self) -> Callable[[str | None], int]:
            return structural_hash

    tags_1: IEnumerable_1[str | None] = distinct(map_2(mapping, tags), ObjectExpr127())
    def chooser(x_2: str | None=None, title: Any=title, tags: Any=tags, selfid: Any=selfid, start_date: Any=start_date, end_date: Any=end_date) -> str | None:
        return x_2

    def _arrow131(__unit: None=None, title: Any=title, tags: Any=tags, selfid: Any=selfid, start_date: Any=start_date, end_date: Any=end_date) -> IEnumerable_1[str | None]:
        def _arrow130(__unit: None=None) -> IEnumerable_1[str | None]:
            def _arrow129(__unit: None=None) -> IEnumerable_1[str | None]:
                def _arrow128(__unit: None=None) -> IEnumerable_1[str | None]:
                    return singleton(end_date)

                return append(singleton(start_date), delay(_arrow128))

            return append(singleton(selfid), delay(_arrow129))

        return append(tags_1, delay(_arrow130))

    metadata: str = join(", ", choose(chooser, to_list(delay(_arrow131))))
    return to_text(printf("%s : %s"))(title)(metadata)


def PieChart_formatData(name: str, value: Any) -> str:
    return to_text(printf("\"%s\" : %A"))(name)(value)


def QuadrantChart_formatAxis(base0: str, req: str, opt: str | None=None) -> str:
    if opt is None:
        return base0 + req

    else: 
        v: str = opt
        return base0 + to_text(printf("%s --> %s"))(req)(v)



def QuadrantChart_formatXAxis(left: str, right: str | None=None) -> str:
    return QuadrantChart_formatAxis("x-axis ", left, right)


def QuadrantChart_formatYAxis(bottom: str, top: str | None=None) -> str:
    return QuadrantChart_formatAxis("y-axis ", bottom, top)


def QuadrantChart_formatPoint(name: str, x: float, y: float) -> str:
    return to_text(printf("%s: [%.2f, %.2f]"))(name)(x)(y)


def Siren_RDRiskType__RDRiskType_ToFormatString(this: RDRiskType) -> str:
    return to_string_1(this).lower()


def Siren_RDVerifyMethod__RDVerifyMethod_ToFormatString(this: RDVerifyMethod) -> str:
    return to_string_1(this).lower()


def Siren_RDRelationship__RDRelationship_ToFormatString(this: RDRelationship) -> str:
    return to_string_1(this).lower()


def RequirementDiagram_createRequirement(type0: str, name: str, id: str | None=None, text: str | None=None, risk: RDRiskType | None=None, methods: RDVerifyMethod | None=None) -> RequirementDiagramElement:
    def mapping_4(Item: str, type0: Any=type0, name: Any=name, id: Any=id, text: Any=text, risk: Any=risk, methods: Any=methods) -> RequirementDiagramElement:
        return RequirementDiagramElement(0, Item)

    def chooser(x: str | None=None, type0: Any=type0, name: Any=name, id: Any=id, text: Any=text, risk: Any=risk, methods: Any=methods) -> str | None:
        return x

    def mapping(i: str, type0: Any=type0, name: Any=name, id: Any=id, text: Any=text, risk: Any=risk, methods: Any=methods) -> str:
        return to_text(printf("id: \"%s\""))(i)

    def mapping_1(t: str, type0: Any=type0, name: Any=name, id: Any=id, text: Any=text, risk: Any=risk, methods: Any=methods) -> str:
        return to_text(printf("text: \"%s\""))(t)

    def mapping_2(r: RDRiskType, type0: Any=type0, name: Any=name, id: Any=id, text: Any=text, risk: Any=risk, methods: Any=methods) -> str:
        arg_2: str = Siren_RDRiskType__RDRiskType_ToFormatString(r)
        return to_text(printf("risk: %s"))(arg_2)

    def mapping_3(m: RDVerifyMethod, type0: Any=type0, name: Any=name, id: Any=id, text: Any=text, risk: Any=risk, methods: Any=methods) -> str:
        arg_3: str = Siren_RDVerifyMethod__RDVerifyMethod_ToFormatString(m)
        return to_text(printf("verifymethod: %s"))(arg_3)

    children: FSharpList[RequirementDiagramElement] = map_1(mapping_4, choose(chooser, of_array([map(mapping, id), map(mapping_1, text), map(mapping_2, risk), map(mapping_3, methods)])))
    return RequirementDiagramElement(1, to_text(printf("%s %s {"))(type0)(name), "}", children)


def RequirementDiagram_createElement(name: str, type0: str | None=None, docref: str | None=None) -> RequirementDiagramElement:
    def mapping_2(Item: str, name: Any=name, type0: Any=type0, docref: Any=docref) -> RequirementDiagramElement:
        return RequirementDiagramElement(0, Item)

    def chooser(x: str | None=None, name: Any=name, type0: Any=type0, docref: Any=docref) -> str | None:
        return x

    def mapping(t: str, name: Any=name, type0: Any=type0, docref: Any=docref) -> str:
        return to_text(printf("type: \"%s\""))(t)

    def mapping_1(d: str, name: Any=name, type0: Any=type0, docref: Any=docref) -> str:
        return to_text(printf("docRef: \"%s\""))(d)

    children: FSharpList[RequirementDiagramElement] = map_1(mapping_2, choose(chooser, of_array([map(mapping, type0), map(mapping_1, docref)])))
    return RequirementDiagramElement(1, to_text(printf("element %s {"))(name), "}", children)


def RequirementDiagram_formatRelationship(id1: str, id2: str, rlts_type: RDRelationship) -> str:
    arg_1: str = Siren_RDRelationship__RDRelationship_ToFormatString(rlts_type)
    return to_text(printf("%s - %s -> %s"))(id1)(arg_1)(id2)


def Siren_GitCommitType__GitCommitType_ToFormatString(this: GitCommitType) -> str:
    return to_string_1(this).upper()


def Git_formatCommitType(commit_type: GitCommitType | None=None) -> str | None:
    def mapping(s: GitCommitType, commit_type: Any=commit_type) -> str:
        arg: str = Siren_GitCommitType__GitCommitType_ToFormatString(s)
        return to_text(printf("type: %s"))(arg)

    return map(mapping, commit_type)


def Git_formatTag(tag: str | None=None) -> str | None:
    def mapping(s: str, tag: Any=tag) -> str:
        return to_text(printf("tag: \"%s\""))(s)

    return map(mapping, tag)


def Git_formatSelfID(selfid: str | None=None) -> str | None:
    def mapping(s: str, selfid: Any=selfid) -> str:
        return to_text(printf("id: \"%s\""))(s)

    return map(mapping, selfid)


def Git_formatParentID(aprent_id: str | None=None) -> str | None:
    def mapping(s: str, aprent_id: Any=aprent_id) -> str:
        return to_text(printf("parent: \"%s\""))(s)

    return map(mapping, aprent_id)


def Git_formatCommit(selfid: str | None=None, commit_type: GitCommitType | None=None, tag: str | None=None) -> str:
    def chooser(x: str | None=None, selfid: Any=selfid, commit_type: Any=commit_type, tag: Any=tag) -> str | None:
        return x

    return join(" ", choose(chooser, of_array(["commit", Git_formatSelfID(selfid), Git_formatCommitType(commit_type), Git_formatTag(tag)])))


def Git_formatMerge(target_id: str, merge_id: str | None=None, commit_type: GitCommitType | None=None, tag: str | None=None) -> str:
    def chooser(x: str | None=None, target_id: Any=target_id, merge_id: Any=merge_id, commit_type: Any=commit_type, tag: Any=tag) -> str | None:
        return x

    return join(" ", choose(chooser, of_array(["merge", target_id, Git_formatSelfID(merge_id), Git_formatCommitType(commit_type), Git_formatTag(tag)])))


def Git_formatCherryPick(commitid: str, parentid: str | None=None) -> str:
    def chooser(x: str | None=None, commitid: Any=commitid, parentid: Any=parentid) -> str | None:
        return x

    return join(" ", choose(chooser, of_array(["cherry-pick", Git_formatSelfID(commitid), Git_formatParentID(parentid)])))


def Mindmap_formatNode(id: str, name: str | None, t: MindmapShape) -> str:
    name_1: str = default_arg(name, id)
    if t.tag == 1:
        return to_text(printf("%s(%s)"))(id)(name_1)

    elif t.tag == 2:
        return to_text(printf("%s((%s))"))(id)(name_1)

    elif t.tag == 3:
        return to_text(printf("%s))%s(("))(id)(name_1)

    elif t.tag == 4:
        return to_text(printf("%s)%s("))(id)(name_1)

    elif t.tag == 5:
        return to_text(printf("%s{{%s}}"))(id)(name_1)

    else: 
        return to_text(printf("%s[%s]"))(id)(name_1)



def Mindmap_handleNodeChildren(children: Any | None, opener: str) -> MindmapElement:
    if (not is_empty(value_1(children))) if (children is not None) else False:
        return MindmapElement(1, opener, "", of_seq(value_1(children)))

    else: 
        return MindmapElement(0, opener)



def Timeline_formatSingle(header: str, data: str | None=None) -> str:
    if data is not None:
        event: str = data
        return to_text(printf("%s : %s"))(header)(event)

    else: 
        return header



def Timeline_createMultiple(header: str, data: FSharpList[str]) -> TimelineElement:
    def mapping(s: str, header: Any=header, data: Any=data) -> TimelineElement:
        return TimelineElement(0, ": " + s)

    return TimelineElement(1, header, "", map_1(mapping, data))


def Sankey_formatLink(source: str, target: str, value: float) -> str:
    source_1: str = replace(source, "\"", "\"\"")
    target_1: str = replace(target, "\"", "\"\"")
    return to_text(printf("\"%s\",\"%s\",%f"))(source_1)(target_1)(value)


def Sankey_createLinks(source: str, targets: FSharpList[tuple[str, float]]) -> SankeyElement:
    def _arrow135(__unit: None=None, source: Any=source, targets: Any=targets) -> IEnumerable_1[SankeyElement]:
        def _arrow134(match_value: tuple[str, float]) -> IEnumerable_1[SankeyElement]:
            return singleton(SankeyElement(0, Sankey_formatLink(source, match_value[0], match_value[1])))

        return collect(_arrow134, targets)

    return SankeyElement(1, to_list(delay(_arrow135)))


def XYChart_formatData(data: FSharpList[str]) -> str:
    return ("[" + join(", ", data)) + "]"


def XYChart_formatXAxis(name: str | None, data: FSharpList[str]) -> str:
    def chooser(x: str | None=None, name: Any=name, data: Any=data) -> str | None:
        return x

    def mapping(name_1: str, name: Any=name, data: Any=data) -> str:
        return to_text(printf("\"%s\""))(name_1)

    return join(" ", choose(chooser, of_array(["x-axis", map(mapping, name), XYChart_formatData(data)])))


def XYChart_formatXAxisRange(name: str | None, data_: float, data__1: float) -> str:
    data: tuple[float, float] = (data_, data__1)
    def chooser(x: str | None=None, name: Any=name, data_: Any=data_, data__1: Any=data__1) -> str | None:
        return x

    def mapping(name_1: str, name: Any=name, data_: Any=data_, data__1: Any=data__1) -> str:
        return to_text(printf("\"%s\""))(name_1)

    return join(" ", choose(chooser, of_array(["x-axis", map(mapping, name), to_text(printf("%f --> %f"))(data[0])(data[1])])))


def XYChart_formatYAxis(name: str | None=None, data: tuple[float, float] | None=None) -> str:
    def chooser(x: str | None=None, name: Any=name, data: Any=data) -> str | None:
        return x

    def mapping(name_1: str, name: Any=name, data: Any=data) -> str:
        return to_text(printf("\"%s\""))(name_1)

    def mapping_1(data_1: tuple[float, float], name: Any=name, data: Any=data) -> str:
        return to_text(printf("%f --> %f"))(data_1[0])(data_1[1])

    return join(" ", choose(chooser, of_array(["y-axis", map(mapping, name), map(mapping_1, data)])))


def XYChart_formatLine(data: FSharpList[float]) -> str:
    def mapping(value: float, data: Any=data) -> str:
        return to_string_1(value)

    arg: str = XYChart_formatData(map_1(mapping, data))
    return to_text(printf("line %s"))(arg)


def XYChart_formatBar(data: FSharpList[float]) -> str:
    def mapping(value: float, data: Any=data) -> str:
        return to_string_1(value)

    arg: str = XYChart_formatData(map_1(mapping, data))
    return to_text(printf("bar %s"))(arg)


def Siren_BlockBlockType__BlockBlockType_ToFormatString_Z384F8060(this: BlockBlockType, id: str, label: str) -> str:
    if this.tag == 1:
        return to_text(printf("%s(\"%s\")"))(id)(label)

    elif this.tag == 2:
        return to_text(printf("%s([\"%s\"])"))(id)(label)

    elif this.tag == 3:
        return to_text(printf("%s[[\"%s\"]]"))(id)(label)

    elif this.tag == 4:
        return to_text(printf("%s[(\"%s\")]"))(id)(label)

    elif this.tag == 5:
        return to_text(printf("%s((\"%s\"))"))(id)(label)

    elif this.tag == 6:
        return to_text(printf("%s>\"%s\"]"))(id)(label)

    elif this.tag == 7:
        return to_text(printf("%s{\"%s\"}"))(id)(label)

    elif this.tag == 8:
        return to_text(printf("%s{{\"%s\"}}"))(id)(label)

    elif this.tag == 9:
        return to_text(printf("%s[/\"%s\"/]"))(id)(label)

    elif this.tag == 10:
        return to_text(printf("%s[\\\"%s\"\\]"))(id)(label)

    elif this.tag == 11:
        return to_text(printf("%s[/\"%s\"\\]"))(id)(label)

    elif this.tag == 12:
        return to_text(printf("%s[\\\"%s\"/]"))(id)(label)

    elif this.tag == 13:
        return to_text(printf("%s(((\"%s\")))"))(id)(label)

    else: 
        return to_text(printf("%s[\"%s\"]"))(id)(label)



def Siren_BlockArrowDirection__BlockArrowDirection_ToFormatString(this: BlockArrowDirection) -> str:
    if this.tag == 6:
        return this.fields[0]

    else: 
        return to_string_1(this).lower()



def Block_formatBlockType(id: str, label: str | None, width: int | None, block_type: BlockBlockType) -> str:
    def mapping(w: int, id: Any=id, label: Any=label, width: Any=width, block_type: Any=block_type) -> str:
        return to_text(printf(":%i"))(w)

    return Siren_BlockBlockType__BlockBlockType_ToFormatString_Z384F8060(block_type, id, default_arg(label, id)) + default_arg(map(mapping, width), "")


def Block_formatBlockArrow(id: str, label: str | None, direction: BlockArrowDirection) -> str:
    label_1: str = default_arg(label, id)
    direction_str: str = Siren_BlockArrowDirection__BlockArrowDirection_ToFormatString(direction)
    return to_text(printf("%s<[\"%s\"]>(%s)"))(id)(label_1)(direction_str)


def Block_formatEmptyBlockArrow(id: str, width: int | None, direction: BlockArrowDirection) -> str:
    def _arrow137(_arg: int, id: Any=id, width: Any=width, direction: Any=direction) -> str:
        return "&nbsp;"

    label_str: str = initialize(default_arg(width, 3), _arrow137)
    direction_str: str = Siren_BlockArrowDirection__BlockArrowDirection_ToFormatString(direction)
    return to_text(printf("%s<[\"%s\"]>(%s)"))(id)(label_str)(direction_str)


def Block_formatSpace(width: int | None=None) -> str:
    if width is not None:
        arg: int = value_1(width) or 0
        return to_text(printf("space:%i"))(arg)

    else: 
        return "space"



def Block_formatLink(id1: str, id2: str, label: str | None=None) -> str:
    if label is not None:
        arg_1: str = value_1(label)
        return to_text(printf("%s-- \"%s\" -->%s"))(id1)(arg_1)(id2)

    else: 
        return to_text(printf("%s-->%s"))(id1)(id2)



def Block_formatStyle(id: str, styles: FSharpList[tuple[str, str]]) -> str:
    def mapping(tupled_arg: tuple[str, str], id: Any=id, styles: Any=styles) -> str:
        return to_text(printf("%s:%s"))(tupled_arg[0])(tupled_arg[1])

    styles_1: str = join(",", map_1(mapping, styles))
    return to_text(printf("style %s %s;"))(id)(styles_1)


def Block_formatClass(node_ids0: FSharpList[str], class_name: str) -> str:
    return trim_end(Generic_formatClass(node_ids0, class_name), ";")


__all__ = ["Siren_NotePosition__NotePosition_ToFormatString", "Generic_formatComment", "Generic_formatDirection", "Generic_formatClickHref", "Generic_formatNote", "Generic_formatClassDef", "Generic_formatClass", "Siren_FlowchartLinkTypes__FlowchartLinkTypes_appendTextOption_Static", "Siren_FlowchartLinkTypes__FlowchartLinkTypes_AddedLengthLinker_71136F3F", "Siren_FlowchartLinkTypes__FlowchartLinkTypes_GetAddLengthChar", "Flowchart_formatMinimalNamedNode", "Flowchart_nodeTypeToFormatter", "Flowchart_formatNode", "Flowchart_formatLinkType", "Flowchart_formatLink", "Flowchart_formatSubgraph", "Flowchart_formatLinkStyles", "Flowchart_formatNodeStyles", "Sequence_formatMessageType", "Sequence_formatMessage", "Sequence_formatParticipant", "Sequence_formatActor", "Sequence_formatCreate", "Sequence_formatDestroy", "Sequence_formatBox", "Sequence_formatNoteSpanning", "Siren_ClassMemberVisibility__ClassMemberVisibility_ToFormatString", "Siren_ClassMemberClassifier__ClassMemberClassifier_ToFormatString", "Siren_ClassRelationshipDirection__ClassRelationshipDirection_ToFormatString_30230F9B", "Siren_ClassRelationshipDirection__ClassRelationshipDirection_ToFormatString_Z384F8060", "Siren_ClassRelationshipType__ClassRelationshipType_ToFormatString_7464358D", "Siren_ClassCardinality__ClassCardinality_ToFormatString", "ClassDiagram_formatClass", "ClassDiagram_formatClassMember", "ClassDiagram_formatGeneric", "ClassDiagram_formatClassAttr", "ClassDiagram_formatClassFunction", "ClassDiagram_formatMember", "ClassDiagram_formatAttr", "ClassDiagram_formatFunction", "ClassDiagram_formatRelationship0", "ClassDiagram_formatRelationship", "ClassDiagram_formatRelationshipCustom", "ClassDiagram_formatAnnotation", "ClassDiagram_formatNote", "ClassDiagram_formatClassStyles", "ClassDiagram_formatCssClass", "StateDiagram_formatState", "StateDiagram_formatTransition", "StateDiagram_formatNoteWrapper", "Siren_ERCardinalityType__ERCardinalityType_ToFormatString", "ERDiagram_formatEntityNode", "ERDiagram_formatEntityWrapper", "ERDiagram_formatAttribute", "ERDiagram_formatRelationship", "UserJourney_formatTask", "Siren_GanttTags__GanttTags_ToFormatString", "Siren_GanttUnit__GanttUnit_ToFormatString", "Gantt_formatTask", "PieChart_formatData", "QuadrantChart_formatAxis", "QuadrantChart_formatXAxis", "QuadrantChart_formatYAxis", "QuadrantChart_formatPoint", "Siren_RDRiskType__RDRiskType_ToFormatString", "Siren_RDVerifyMethod__RDVerifyMethod_ToFormatString", "Siren_RDRelationship__RDRelationship_ToFormatString", "RequirementDiagram_createRequirement", "RequirementDiagram_createElement", "RequirementDiagram_formatRelationship", "Siren_GitCommitType__GitCommitType_ToFormatString", "Git_formatCommitType", "Git_formatTag", "Git_formatSelfID", "Git_formatParentID", "Git_formatCommit", "Git_formatMerge", "Git_formatCherryPick", "Mindmap_formatNode", "Mindmap_handleNodeChildren", "Timeline_formatSingle", "Timeline_createMultiple", "Sankey_formatLink", "Sankey_createLinks", "XYChart_formatData", "XYChart_formatXAxis", "XYChart_formatXAxisRange", "XYChart_formatYAxis", "XYChart_formatLine", "XYChart_formatBar", "Siren_BlockBlockType__BlockBlockType_ToFormatString_Z384F8060", "Siren_BlockArrowDirection__BlockArrowDirection_ToFormatString", "Block_formatBlockType", "Block_formatBlockArrow", "Block_formatEmptyBlockArrow", "Block_formatSpace", "Block_formatLink", "Block_formatStyle", "Block_formatClass"]

