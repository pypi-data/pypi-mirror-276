from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from .fable-library.list import (of_seq, singleton, map, FSharpList, empty as empty_1, cons, of_array)
from .fable-library.option import (value as value_1, default_arg, map as map_2, some)
from .fable-library.range import range_big_int
from .fable-library.reflection import (TypeInfo, class_type)
from .fable-library.seq import (length, to_list, delay, append, singleton as singleton_1, collect, item, empty, is_empty, map as map_1)
from .fable-library.string_ import (to_text, printf, join, split)
from .fable-library.types import Array
from .fable-library.util import (IEnumerable_1, equals)
from .formatting import (Generic_formatComment, Flowchart_formatNode, Flowchart_formatLink, Generic_formatDirection, Flowchart_formatSubgraph, Generic_formatClickHref, Flowchart_formatLinkStyles, Flowchart_formatNodeStyles, Generic_formatClassDef, Generic_formatClass, Sequence_formatParticipant, Sequence_formatActor, Sequence_formatCreate, Sequence_formatDestroy, Sequence_formatBox, Sequence_formatMessage, Generic_formatNote, Sequence_formatNoteSpanning, ClassDiagram_formatClass, ClassDiagram_formatClassMember, ClassDiagram_formatClassAttr, ClassDiagram_formatClassFunction, ClassDiagram_formatMember, ClassDiagram_formatAttr, ClassDiagram_formatFunction, ClassDiagram_formatRelationship, ClassDiagram_formatRelationshipCustom, ClassDiagram_formatAnnotation, ClassDiagram_formatNote, ClassDiagram_formatClassStyles, ClassDiagram_formatCssClass, StateDiagram_formatState, StateDiagram_formatTransition, StateDiagram_formatNoteWrapper, ERDiagram_formatAttribute, ERDiagram_formatEntityWrapper, ERDiagram_formatEntityNode, ERDiagram_formatRelationship, UserJourney_formatTask, Gantt_formatTask, Siren_GanttUnit__GanttUnit_ToFormatString, PieChart_formatData, QuadrantChart_formatXAxis, QuadrantChart_formatYAxis, QuadrantChart_formatPoint, RequirementDiagram_createRequirement, RequirementDiagram_createElement, RequirementDiagram_formatRelationship, Git_formatCommit, Git_formatMerge, Git_formatCherryPick, Mindmap_handleNodeChildren, Mindmap_formatNode, Timeline_formatSingle, Timeline_createMultiple, Sankey_formatLink, Sankey_createLinks, XYChart_formatXAxis, XYChart_formatXAxisRange, XYChart_formatYAxis, XYChart_formatLine, XYChart_formatBar, Block_formatBlockType, Block_formatBlockArrow, Block_formatEmptyBlockArrow, Block_formatSpace, Block_formatLink, Block_formatStyle, Block_formatClass)
from .siren_types import (Direction, FlowchartElement, FlowchartNodeTypes, FlowchartLinkTypes, NotePosition, SequenceElement, SequenceMessageTypes, ClassMemberVisibility, ClassMemberClassifier, ClassRelationshipDirection, ClassCardinality, ClassRelationshipType, ClassDiagramElement, StateDiagramElement, ERKeyType, ERCardinalityType, ERDiagramElement, ERAttribute, JourneyElement, GanttTags, GanttUnit, GanttElement, PieChartElement, QuadrantElement, RDRiskType, RDVerifyMethod, RequirementDiagramElement, RDRelationship, GitCommitType, GitGraphElement, MindmapElement, MindmapShape, TimelineElement, SankeyElement, XYChartElement, BlockElement, BlockBlockType, BlockArrowDirection, SirenGraph, SirenElement, ConfigVariable, ThemeVariable)
from .util import Option_defaultBind
from .yaml import (Yaml_write, Yaml_root)

__M = TypeVar("__M")

__I = TypeVar("__I")

__F = TypeVar("__F")

__A = TypeVar("__A")

__E = TypeVar("__E")

__D = TypeVar("__D")

__C = TypeVar("__C")

__B = TypeVar("__B")

def _expr154() -> TypeInfo:
    return class_type("Siren.formatting", None, formatting)


class formatting:
    @staticmethod
    def unicode(txt: str) -> str:
        return ("\"" + txt) + "\""

    @staticmethod
    def markdown(txt: str) -> str:
        return ("\"`" + txt) + "`\""

    @staticmethod
    def comment(txt: str) -> str:
        return Generic_formatComment(txt)

    @staticmethod
    def protected_whitespace() -> str:
        return "&nbsp;"


formatting_reflection = _expr154

def _expr155() -> TypeInfo:
    return class_type("Siren.direction", None, direction)


class direction:
    @staticmethod
    def tb() -> Direction:
        return Direction(0)

    @staticmethod
    def td() -> Direction:
        return Direction(1)

    @staticmethod
    def bt() -> Direction:
        return Direction(2)

    @staticmethod
    def rl() -> Direction:
        return Direction(3)

    @staticmethod
    def lr() -> Direction:
        return Direction(4)

    @staticmethod
    def top_to_bottom() -> Direction:
        return direction.tb()

    @staticmethod
    def top_down() -> Direction:
        return direction.td()

    @staticmethod
    def bottom_to_top() -> Direction:
        return direction.bt()

    @staticmethod
    def right_to_left() -> Direction:
        return direction.rl()

    @staticmethod
    def left_to_right() -> Direction:
        return direction.lr()

    @staticmethod
    def custom(str_1: str) -> Direction:
        return Direction(5, str_1)


direction_reflection = _expr155

def _expr156() -> TypeInfo:
    return class_type("Siren.flowchart", None, flowchart)


class flowchart:
    @staticmethod
    def raw(txt: str) -> FlowchartElement:
        return FlowchartElement(0, txt)

    @staticmethod
    def id(txt: str) -> FlowchartElement:
        return FlowchartElement(0, txt)

    @staticmethod
    def node(id: str, name: str | None=None) -> FlowchartElement:
        return FlowchartElement(0, Flowchart_formatNode(id, name, FlowchartNodeTypes(0)))

    @staticmethod
    def node_round(id: str, name: str | None=None) -> FlowchartElement:
        return FlowchartElement(0, Flowchart_formatNode(id, name, FlowchartNodeTypes(1)))

    @staticmethod
    def node_stadium(id: str, name: str | None=None) -> FlowchartElement:
        return FlowchartElement(0, Flowchart_formatNode(id, name, FlowchartNodeTypes(2)))

    @staticmethod
    def node_subroutine(id: str, name: str | None=None) -> FlowchartElement:
        return FlowchartElement(0, Flowchart_formatNode(id, name, FlowchartNodeTypes(3)))

    @staticmethod
    def node_cylindrical(id: str, name: str | None=None) -> FlowchartElement:
        return FlowchartElement(0, Flowchart_formatNode(id, name, FlowchartNodeTypes(4)))

    @staticmethod
    def node_circle(id: str, name: str | None=None) -> FlowchartElement:
        return FlowchartElement(0, Flowchart_formatNode(id, name, FlowchartNodeTypes(5)))

    @staticmethod
    def node_asymmetric(id: str, name: str | None=None) -> FlowchartElement:
        return FlowchartElement(0, Flowchart_formatNode(id, name, FlowchartNodeTypes(6)))

    @staticmethod
    def node_rhombus(id: str, name: str | None=None) -> FlowchartElement:
        return FlowchartElement(0, Flowchart_formatNode(id, name, FlowchartNodeTypes(7)))

    @staticmethod
    def node_hexagon(id: str, name: str | None=None) -> FlowchartElement:
        return FlowchartElement(0, Flowchart_formatNode(id, name, FlowchartNodeTypes(8)))

    @staticmethod
    def node_parallelogram(id: str, name: str | None=None) -> FlowchartElement:
        return FlowchartElement(0, Flowchart_formatNode(id, name, FlowchartNodeTypes(9)))

    @staticmethod
    def node_parallelogram_alt(id: str, name: str | None=None) -> FlowchartElement:
        return FlowchartElement(0, Flowchart_formatNode(id, name, FlowchartNodeTypes(10)))

    @staticmethod
    def node_trapezoid(id: str, name: str | None=None) -> FlowchartElement:
        return FlowchartElement(0, Flowchart_formatNode(id, name, FlowchartNodeTypes(11)))

    @staticmethod
    def node_trapezoid_alt(id: str, name: str | None=None) -> FlowchartElement:
        return FlowchartElement(0, Flowchart_formatNode(id, name, FlowchartNodeTypes(12)))

    @staticmethod
    def node_double_circle(id: str, name: str | None=None) -> FlowchartElement:
        return FlowchartElement(0, Flowchart_formatNode(id, name, FlowchartNodeTypes(13)))

    @staticmethod
    def link_arrow(id1: str, id2: str, message: str | None=None, added_length: int | None=None) -> FlowchartElement:
        return FlowchartElement(0, Flowchart_formatLink(id1, id2, FlowchartLinkTypes(0), message, added_length))

    @staticmethod
    def link_arrow_double(id1: str, id2: str, message: str | None=None, added_length: int | None=None) -> FlowchartElement:
        return FlowchartElement(0, Flowchart_formatLink(id1, id2, FlowchartLinkTypes(9), message, added_length))

    @staticmethod
    def link_open(id1: str, id2: str, message: str | None=None, added_length: int | None=None) -> FlowchartElement:
        return FlowchartElement(0, Flowchart_formatLink(id1, id2, FlowchartLinkTypes(1), message, added_length))

    @staticmethod
    def link_dotted(id1: str, id2: str, message: str | None=None, added_length: int | None=None) -> FlowchartElement:
        return FlowchartElement(0, Flowchart_formatLink(id1, id2, FlowchartLinkTypes(2), message, added_length))

    @staticmethod
    def link_dotted_arrow(id1: str, id2: str, message: str | None=None, added_length: int | None=None) -> FlowchartElement:
        return FlowchartElement(0, Flowchart_formatLink(id1, id2, FlowchartLinkTypes(3), message, added_length))

    @staticmethod
    def link_thick(id1: str, id2: str, message: str | None=None, added_length: int | None=None) -> FlowchartElement:
        return FlowchartElement(0, Flowchart_formatLink(id1, id2, FlowchartLinkTypes(4), message, added_length))

    @staticmethod
    def link_thick_arrow(id1: str, id2: str, message: str | None=None, added_length: int | None=None) -> FlowchartElement:
        return FlowchartElement(0, Flowchart_formatLink(id1, id2, FlowchartLinkTypes(5), message, added_length))

    @staticmethod
    def link_invisible(id1: str, id2: str, message: str | None=None, added_length: int | None=None) -> FlowchartElement:
        return FlowchartElement(0, Flowchart_formatLink(id1, id2, FlowchartLinkTypes(6), message, added_length))

    @staticmethod
    def link_circle_edge(id1: str, id2: str, message: str | None=None, added_length: int | None=None) -> FlowchartElement:
        return FlowchartElement(0, Flowchart_formatLink(id1, id2, FlowchartLinkTypes(7), message, added_length))

    @staticmethod
    def link_circle_double(id1: str, id2: str, message: str | None=None, added_length: int | None=None) -> FlowchartElement:
        return FlowchartElement(0, Flowchart_formatLink(id1, id2, FlowchartLinkTypes(10), message, added_length))

    @staticmethod
    def link_cross_edge(id1: str, id2: str, message: str | None=None, added_length: int | None=None) -> FlowchartElement:
        return FlowchartElement(0, Flowchart_formatLink(id1, id2, FlowchartLinkTypes(8), message, added_length))

    @staticmethod
    def link_cross_double(id1: str, id2: str, message: str | None=None, added_length: int | None=None) -> FlowchartElement:
        return FlowchartElement(0, Flowchart_formatLink(id1, id2, FlowchartLinkTypes(11), message, added_length))

    @staticmethod
    def direction(direction_1: Direction) -> FlowchartElement:
        return FlowchartElement(0, Generic_formatDirection(direction_1))

    @staticmethod
    def direction_tb() -> FlowchartElement:
        return FlowchartElement(0, Generic_formatDirection(Direction(0)))

    @staticmethod
    def direction_td() -> FlowchartElement:
        return FlowchartElement(0, Generic_formatDirection(Direction(1)))

    @staticmethod
    def direction_bt() -> FlowchartElement:
        return FlowchartElement(0, Generic_formatDirection(Direction(2)))

    @staticmethod
    def direction_rl() -> FlowchartElement:
        return FlowchartElement(0, Generic_formatDirection(Direction(3)))

    @staticmethod
    def direction_lr() -> FlowchartElement:
        return FlowchartElement(0, Generic_formatDirection(Direction(4)))

    @staticmethod
    def subgraph_named(id: str, name: str, children: Any) -> FlowchartElement:
        return FlowchartElement(1, Flowchart_formatSubgraph(id, name), "end", of_seq(children))

    @staticmethod
    def subgraph(id: str, children: Any) -> FlowchartElement:
        return FlowchartElement(1, Flowchart_formatSubgraph(id, None), "end", of_seq(children))

    @staticmethod
    def click_href(id: str, url: str, tooltip: str | None=None) -> FlowchartElement:
        return FlowchartElement(0, Generic_formatClickHref(id, url, tooltip))

    @staticmethod
    def comment(txt: str) -> FlowchartElement:
        return FlowchartElement(0, Generic_formatComment(txt))

    @staticmethod
    def styles_link(link_order_id: int, styles: Any) -> FlowchartElement:
        return FlowchartElement(0, Flowchart_formatLinkStyles(singleton(link_order_id), of_seq(styles)))

    @staticmethod
    def styles_links(link_order_ids: Any, styles: Any) -> FlowchartElement:
        return FlowchartElement(0, Flowchart_formatLinkStyles(of_seq(link_order_ids), of_seq(styles)))

    @staticmethod
    def styles_node(node_id: str, styles: Any) -> FlowchartElement:
        return FlowchartElement(0, Flowchart_formatNodeStyles(singleton(node_id), of_seq(styles)))

    @staticmethod
    def class_def(class_name: str, styles: Any) -> FlowchartElement:
        return FlowchartElement(0, Generic_formatClassDef(class_name, of_seq(styles)))

    @staticmethod
    def class_(node_ids: Any, class_name: str) -> FlowchartElement:
        return FlowchartElement(0, Generic_formatClass(of_seq(node_ids), class_name))


flowchart_reflection = _expr156

def _expr157() -> TypeInfo:
    return class_type("Siren.notePosition", None, notePosition)


class note_position:
    @staticmethod
    def over() -> NotePosition:
        return NotePosition(0)

    @staticmethod
    def right_of() -> NotePosition:
        return NotePosition(1)

    @staticmethod
    def left_of() -> NotePosition:
        return NotePosition(2)


notePosition_reflection = _expr157

def _expr167() -> TypeInfo:
    return class_type("Siren.sequence", None, sequence)


class sequence:
    @staticmethod
    def raw(txt: str) -> SequenceElement:
        return SequenceElement(0, txt)

    @staticmethod
    def participant(name: str, alias: str | None=None) -> SequenceElement:
        return SequenceElement(0, Sequence_formatParticipant(name, alias))

    @staticmethod
    def actor(name: str, alias: str | None=None) -> SequenceElement:
        return SequenceElement(0, Sequence_formatActor(name, alias))

    @staticmethod
    def create_participant(name: str, alias: str | None=None) -> SequenceElement:
        return SequenceElement(0, Sequence_formatCreate(Sequence_formatParticipant, name, alias))

    @staticmethod
    def create_actor(name: str, alias: str | None=None) -> SequenceElement:
        return SequenceElement(0, Sequence_formatCreate(Sequence_formatActor, name, alias))

    @staticmethod
    def destroy(id: str) -> SequenceElement:
        return SequenceElement(0, Sequence_formatDestroy(id))

    @staticmethod
    def box(name: str, children: Any) -> SequenceElement:
        return SequenceElement(1, Sequence_formatBox(name, None), "end", of_seq(children))

    @staticmethod
    def box_colored(name: str, color: str, children: Any) -> SequenceElement:
        return SequenceElement(1, Sequence_formatBox(name, color), "end", of_seq(children))

    @staticmethod
    def message(a1: str, a2: str, message: str, activate: bool | None=None) -> SequenceElement:
        return SequenceElement(0, Sequence_formatMessage(a1, a2, SequenceMessageTypes(0), message, activate))

    @staticmethod
    def message_solid(a1: str, a2: str, message: str, activate: bool | None=None) -> SequenceElement:
        return SequenceElement(0, Sequence_formatMessage(a1, a2, SequenceMessageTypes(0), message, activate))

    @staticmethod
    def message_dotted(a1: str, a2: str, message: str, activate: bool | None=None) -> SequenceElement:
        return SequenceElement(0, Sequence_formatMessage(a1, a2, SequenceMessageTypes(1), message, activate))

    @staticmethod
    def message_arrow(a1: str, a2: str, message: str, activate: bool | None=None) -> SequenceElement:
        return SequenceElement(0, Sequence_formatMessage(a1, a2, SequenceMessageTypes(2), message, activate))

    @staticmethod
    def message_dotted_arrow(a1: str, a2: str, message: str, activate: bool | None=None) -> SequenceElement:
        return SequenceElement(0, Sequence_formatMessage(a1, a2, SequenceMessageTypes(3), message, activate))

    @staticmethod
    def message_cross(a1: str, a2: str, message: str, activate: bool | None=None) -> SequenceElement:
        return SequenceElement(0, Sequence_formatMessage(a1, a2, SequenceMessageTypes(4), message, activate))

    @staticmethod
    def message_dotted_cross(a1: str, a2: str, message: str, activate: bool | None=None) -> SequenceElement:
        return SequenceElement(0, Sequence_formatMessage(a1, a2, SequenceMessageTypes(5), message, activate))

    @staticmethod
    def message_open_arrow(a1: str, a2: str, message: str, activate: bool | None=None) -> SequenceElement:
        return SequenceElement(0, Sequence_formatMessage(a1, a2, SequenceMessageTypes(6), message, activate))

    @staticmethod
    def message_dotted_open_arrow(a1: str, a2: str, message: str, activate: bool | None=None) -> SequenceElement:
        return SequenceElement(0, Sequence_formatMessage(a1, a2, SequenceMessageTypes(7), message, activate))

    @staticmethod
    def activate(id: str) -> SequenceElement:
        return SequenceElement(0, to_text(printf("activate %s"))(id))

    @staticmethod
    def deactivate(id: str) -> SequenceElement:
        return SequenceElement(0, to_text(printf("deactivate %s"))(id))

    @staticmethod
    def note(id: str, text: str, note_position: NotePosition | None=None) -> SequenceElement:
        return SequenceElement(0, Generic_formatNote(id, note_position, text))

    @staticmethod
    def note_spanning(id1: str, id2: str, text: str, note_position: NotePosition | None=None) -> SequenceElement:
        return SequenceElement(0, Sequence_formatNoteSpanning(id1, id2, note_position, text))

    @staticmethod
    def loop(name: str, children: Any) -> SequenceElement:
        return SequenceElement(1, to_text(printf("loop %s"))(name), "end", of_seq(children))

    @staticmethod
    def alt(name: str, children: Any, else_list: Any) -> SequenceElement:
        else_items: int = length(else_list) or 0
        alt_closer: str = "end" if (else_items == 0) else ""
        last: int = (else_items - 1) or 0
        def _arrow160(__unit: None=None) -> IEnumerable_1[SequenceElement]:
            def _arrow159(__unit: None=None) -> IEnumerable_1[SequenceElement]:
                def _arrow158(i: int) -> IEnumerable_1[SequenceElement]:
                    pattern_input: tuple[str, __M] = item(i, else_list)
                    closer: str = "end" if (i == last) else ""
                    return singleton_1(SequenceElement(1, to_text(printf("else %s"))(pattern_input[0]), closer, of_seq(pattern_input[1])))

                return collect(_arrow158, range_big_int(0, 1, last)) if (else_items != 0) else empty()

            return append(singleton_1(SequenceElement(1, to_text(printf("alt %s"))(name), alt_closer, of_seq(children))), delay(_arrow159))

        return SequenceElement(2, to_list(delay(_arrow160)))

    @staticmethod
    def opt(name: str, children: Any) -> SequenceElement:
        return SequenceElement(1, to_text(printf("opt %s"))(name), "end", of_seq(children))

    @staticmethod
    def par(name: str, children: Any, and_list: Any) -> SequenceElement:
        else_items: int = length(and_list) or 0
        alt_closer: str = "end" if (else_items == 0) else ""
        last: int = (else_items - 1) or 0
        def _arrow163(__unit: None=None) -> IEnumerable_1[SequenceElement]:
            def _arrow162(__unit: None=None) -> IEnumerable_1[SequenceElement]:
                def _arrow161(i: int) -> IEnumerable_1[SequenceElement]:
                    pattern_input: tuple[str, __I] = item(i, and_list)
                    closer: str = "end" if (i == last) else ""
                    return singleton_1(SequenceElement(1, to_text(printf("and %s"))(pattern_input[0]), closer, of_seq(pattern_input[1])))

                return collect(_arrow161, range_big_int(0, 1, last)) if (else_items != 0) else empty()

            return append(singleton_1(SequenceElement(1, to_text(printf("par %s"))(name), alt_closer, of_seq(children))), delay(_arrow162))

        return SequenceElement(2, to_list(delay(_arrow163)))

    @staticmethod
    def critical(name: str, children: Any, option_list: Any) -> SequenceElement:
        else_items: int = length(option_list) or 0
        alt_closer: str = "end" if (else_items == 0) else ""
        last: int = (else_items - 1) or 0
        def _arrow166(__unit: None=None) -> IEnumerable_1[SequenceElement]:
            def _arrow165(__unit: None=None) -> IEnumerable_1[SequenceElement]:
                def _arrow164(i: int) -> IEnumerable_1[SequenceElement]:
                    pattern_input: tuple[str, __F] = item(i, option_list)
                    closer: str = "end" if (i == last) else ""
                    return singleton_1(SequenceElement(1, to_text(printf("option %s"))(pattern_input[0]), closer, of_seq(pattern_input[1])))

                return collect(_arrow164, range_big_int(0, 1, last)) if (else_items != 0) else empty()

            return append(singleton_1(SequenceElement(1, to_text(printf("critical %s"))(name), alt_closer, of_seq(children))), delay(_arrow165))

        return SequenceElement(2, to_list(delay(_arrow166)))

    @staticmethod
    def break_seq(name: str, children: Any) -> SequenceElement:
        return SequenceElement(1, to_text(printf("break %s"))(name), "end", of_seq(children))

    @staticmethod
    def rect(color: str, children: Any) -> SequenceElement:
        return SequenceElement(1, to_text(printf("rect %s"))(color), "end", of_seq(children))

    @staticmethod
    def comment(txt: str) -> SequenceElement:
        return SequenceElement(0, Generic_formatComment(txt))

    @staticmethod
    def auto_number() -> SequenceElement:
        return SequenceElement(0, "autonumber")

    @staticmethod
    def link(id: str, url_label: str, url: str) -> SequenceElement:
        return SequenceElement(0, to_text(printf("link %s: %s @ %s"))(id)(url_label)(url))

    @staticmethod
    def links(id: str, urls: Any) -> SequenceElement:
        def mapping(tupled_arg: tuple[str, str]) -> str:
            return to_text(printf("\"%s\": \"%s\""))(tupled_arg[0])(tupled_arg[1])

        json: str = ("{" + join(", ", map(mapping, of_seq(urls)))) + "}"
        return SequenceElement(0, to_text(printf("links %s: %s"))(id)(json))


sequence_reflection = _expr167

def _expr168() -> TypeInfo:
    return class_type("Siren.classMemberVisibility", None, classMemberVisibility)


class class_member_visibility:
    @staticmethod
    def Public() -> ClassMemberVisibility:
        return ClassMemberVisibility(0)

    @staticmethod
    def Private() -> ClassMemberVisibility:
        return ClassMemberVisibility(1)

    @staticmethod
    def Protected() -> ClassMemberVisibility:
        return ClassMemberVisibility(2)

    @staticmethod
    def package_internal() -> ClassMemberVisibility:
        return ClassMemberVisibility(3)

    @staticmethod
    def custom(str_1: str) -> ClassMemberVisibility:
        return ClassMemberVisibility(4, str_1)


classMemberVisibility_reflection = _expr168

def _expr169() -> TypeInfo:
    return class_type("Siren.classMemberClassifier", None, classMemberClassifier)


class class_member_classifier:
    @staticmethod
    def Abstract() -> ClassMemberClassifier:
        return ClassMemberClassifier(0)

    @staticmethod
    def Static() -> ClassMemberClassifier:
        return ClassMemberClassifier(1)

    @staticmethod
    def custom(str_1: str) -> ClassMemberClassifier:
        return ClassMemberClassifier(2, str_1)


classMemberClassifier_reflection = _expr169

def _expr170() -> TypeInfo:
    return class_type("Siren.classDirection", None, classDirection)


class class_direction:
    @staticmethod
    def two_way() -> ClassRelationshipDirection:
        return ClassRelationshipDirection(2)

    @staticmethod
    def left() -> ClassRelationshipDirection:
        return ClassRelationshipDirection(0)

    @staticmethod
    def right() -> ClassRelationshipDirection:
        return ClassRelationshipDirection(1)


classDirection_reflection = _expr170

def _expr171() -> TypeInfo:
    return class_type("Siren.classCardinality", None, classCardinality)


class class_cardinality:
    @staticmethod
    def n() -> ClassCardinality:
        return ClassCardinality(4)

    @staticmethod
    def many() -> ClassCardinality:
        return ClassCardinality(3)

    @staticmethod
    def one() -> ClassCardinality:
        return ClassCardinality(0)

    @staticmethod
    def one_or_more() -> ClassCardinality:
        return ClassCardinality(2)

    @staticmethod
    def one_to_n() -> ClassCardinality:
        return ClassCardinality(6)

    @staticmethod
    def zero_or_one() -> ClassCardinality:
        return ClassCardinality(1)

    @staticmethod
    def zero_to_n() -> ClassCardinality:
        return ClassCardinality(5)

    @staticmethod
    def custom(cardinality: str) -> ClassCardinality:
        return ClassCardinality(7, cardinality)


classCardinality_reflection = _expr171

def _expr172() -> TypeInfo:
    return class_type("Siren.classRltsType", None, classRltsType)


class class_rlts_type:
    @staticmethod
    def inheritance() -> ClassRelationshipType:
        return ClassRelationshipType(0)

    @staticmethod
    def aggregation() -> ClassRelationshipType:
        return ClassRelationshipType(2)

    @staticmethod
    def association() -> ClassRelationshipType:
        return ClassRelationshipType(3)

    @staticmethod
    def composition() -> ClassRelationshipType:
        return ClassRelationshipType(1)

    @staticmethod
    def dashed() -> ClassRelationshipType:
        return ClassRelationshipType(6)

    @staticmethod
    def dependency() -> ClassRelationshipType:
        return ClassRelationshipType(7)

    @staticmethod
    def link() -> ClassRelationshipType:
        return ClassRelationshipType(4)

    @staticmethod
    def realization() -> ClassRelationshipType:
        return ClassRelationshipType(8)

    @staticmethod
    def solid() -> ClassRelationshipType:
        return ClassRelationshipType(5)


classRltsType_reflection = _expr172

def _expr173() -> TypeInfo:
    return class_type("Siren.classDiagram", None, classDiagram)


class class_diagram:
    @staticmethod
    def raw(txt: str) -> ClassDiagramElement:
        return ClassDiagramElement(0, txt)

    @staticmethod
    def class_(id: str, members: Any) -> ClassDiagramElement:
        return ClassDiagramElement(1, ClassDiagram_formatClass(id, None, None) + "{", "}", of_seq(members))

    @staticmethod
    def class_id(id: str, name: str | None=None, generic: str | None=None, members: Any | None=None) -> ClassDiagramElement:
        return ClassDiagramElement(1, ClassDiagram_formatClass(id, name, generic) + "{", "}", of_seq(value_1(members))) if (members is not None) else ClassDiagramElement(0, ClassDiagram_formatClass(id, name, generic))

    @staticmethod
    def class_member(name: str, class_member_visibility: ClassMemberVisibility | None=None, class_member_classifier: ClassMemberClassifier | None=None) -> ClassDiagramElement:
        return ClassDiagramElement(0, ClassDiagram_formatClassMember(name, class_member_visibility, class_member_classifier))

    @staticmethod
    def class_attr(name: str, generic: str | None=None, class_member_visibility: ClassMemberVisibility | None=None, class_member_classifier: ClassMemberClassifier | None=None) -> ClassDiagramElement:
        return ClassDiagramElement(0, ClassDiagram_formatClassAttr(name, generic, class_member_visibility, class_member_classifier))

    @staticmethod
    def class_function(name: str, param: str | None=None, return_type: str | None=None, class_member_visibility: ClassMemberVisibility | None=None, class_member_classifier: ClassMemberClassifier | None=None) -> ClassDiagramElement:
        return ClassDiagramElement(0, ClassDiagram_formatClassFunction(name, param, return_type, class_member_visibility, class_member_classifier))

    @staticmethod
    def id_member(id: str, name: str, class_member_visibility: ClassMemberVisibility | None=None, class_member_classifier: ClassMemberClassifier | None=None) -> ClassDiagramElement:
        return ClassDiagramElement(0, ClassDiagram_formatMember(id, name, class_member_visibility, class_member_classifier))

    @staticmethod
    def id_attr(id: str, name: str, generic: str | None=None, class_member_visibility: ClassMemberVisibility | None=None, class_member_classifier: ClassMemberClassifier | None=None) -> ClassDiagramElement:
        return ClassDiagramElement(0, ClassDiagram_formatAttr(id, name, generic, class_member_visibility, class_member_classifier))

    @staticmethod
    def id_function(id: str, name: str, param: str | None=None, return_type: str | None=None, class_member_visibility: ClassMemberVisibility | None=None, class_member_classifier: ClassMemberClassifier | None=None) -> ClassDiagramElement:
        return ClassDiagramElement(0, ClassDiagram_formatFunction(id, name, param, return_type, class_member_visibility, class_member_classifier))

    @staticmethod
    def relationship_inheritance(id1: str, id2: str, label: str | None=None, cardinality1: ClassCardinality | None=None, cardinality2: ClassCardinality | None=None) -> ClassDiagramElement:
        return ClassDiagramElement(0, ClassDiagram_formatRelationship(id1, id2, ClassRelationshipType(0), label, cardinality1, cardinality2))

    @staticmethod
    def relationship_composition(id1: str, id2: str, label: str | None=None, cardinality1: ClassCardinality | None=None, cardinality2: ClassCardinality | None=None) -> ClassDiagramElement:
        return ClassDiagramElement(0, ClassDiagram_formatRelationship(id1, id2, ClassRelationshipType(1), label, cardinality1, cardinality2))

    @staticmethod
    def relationship_aggregation(id1: str, id2: str, label: str | None=None, cardinality1: ClassCardinality | None=None, cardinality2: ClassCardinality | None=None) -> ClassDiagramElement:
        return ClassDiagramElement(0, ClassDiagram_formatRelationship(id1, id2, ClassRelationshipType(2), label, cardinality1, cardinality2))

    @staticmethod
    def relationship_association(id1: str, id2: str, label: str | None=None, cardinality1: ClassCardinality | None=None, cardinality2: ClassCardinality | None=None) -> ClassDiagramElement:
        return ClassDiagramElement(0, ClassDiagram_formatRelationship(id1, id2, ClassRelationshipType(3), label, cardinality1, cardinality2))

    @staticmethod
    def relationship_solid(id1: str, id2: str, label: str | None=None, cardinality1: ClassCardinality | None=None, cardinality2: ClassCardinality | None=None) -> ClassDiagramElement:
        return ClassDiagramElement(0, ClassDiagram_formatRelationship(id1, id2, ClassRelationshipType(5), label, cardinality1, cardinality2))

    @staticmethod
    def relationship_dependency(id1: str, id2: str, label: str | None=None, cardinality1: ClassCardinality | None=None, cardinality2: ClassCardinality | None=None) -> ClassDiagramElement:
        return ClassDiagramElement(0, ClassDiagram_formatRelationship(id1, id2, ClassRelationshipType(7), label, cardinality1, cardinality2))

    @staticmethod
    def relationship_realization(id1: str, id2: str, label: str | None=None, cardinality1: ClassCardinality | None=None, cardinality2: ClassCardinality | None=None) -> ClassDiagramElement:
        return ClassDiagramElement(0, ClassDiagram_formatRelationship(id1, id2, ClassRelationshipType(8), label, cardinality1, cardinality2))

    @staticmethod
    def relationship_dashed(id1: str, id2: str, label: str | None=None, cardinality1: ClassCardinality | None=None, cardinality2: ClassCardinality | None=None) -> ClassDiagramElement:
        return ClassDiagramElement(0, ClassDiagram_formatRelationship(id1, id2, ClassRelationshipType(6), label, cardinality1, cardinality2))

    @staticmethod
    def relationship_custom(id1: str, id2: str, rlts_type: ClassRelationshipType, label: str | None=None, direction_1: ClassRelationshipDirection | None=None, is_dotted: bool | None=None, cardinality1: ClassCardinality | None=None, cardinality2: ClassCardinality | None=None) -> ClassDiagramElement:
        return ClassDiagramElement(0, ClassDiagram_formatRelationshipCustom(id1, id2, rlts_type, direction_1, is_dotted, label, cardinality1, cardinality2))

    @staticmethod
    def namespace(name: str, children: Any) -> ClassDiagramElement:
        return ClassDiagramElement(2) if is_empty(children) else ClassDiagramElement(1, to_text(printf("namespace %s {"))(name), "}", of_seq(children))

    @staticmethod
    def Interface(id: str | None=None) -> ClassDiagramElement:
        return ClassDiagramElement(0, ClassDiagram_formatAnnotation(id, "Interface"))

    @staticmethod
    def Abstract(id: str | None=None) -> ClassDiagramElement:
        return ClassDiagramElement(0, ClassDiagram_formatAnnotation(id, "Abstract"))

    @staticmethod
    def service(id: str | None=None) -> ClassDiagramElement:
        return ClassDiagramElement(0, ClassDiagram_formatAnnotation(id, "Service"))

    @staticmethod
    def enumeration(id: str | None=None) -> ClassDiagramElement:
        return ClassDiagramElement(0, ClassDiagram_formatAnnotation(id, "Enumeration"))

    @staticmethod
    def annotation(name: str, id: str | None=None) -> ClassDiagramElement:
        return ClassDiagramElement(0, ClassDiagram_formatAnnotation(id, name))

    @staticmethod
    def comment(txt: str) -> ClassDiagramElement:
        return ClassDiagramElement(0, Generic_formatComment(txt))

    @staticmethod
    def direction(direction_1: Direction) -> ClassDiagramElement:
        return ClassDiagramElement(0, Generic_formatDirection(direction_1))

    @staticmethod
    def direction_tb() -> ClassDiagramElement:
        return ClassDiagramElement(0, Generic_formatDirection(Direction(0)))

    @staticmethod
    def direction_td() -> ClassDiagramElement:
        return ClassDiagramElement(0, Generic_formatDirection(Direction(1)))

    @staticmethod
    def direction_bt() -> ClassDiagramElement:
        return ClassDiagramElement(0, Generic_formatDirection(Direction(2)))

    @staticmethod
    def direction_rl() -> ClassDiagramElement:
        return ClassDiagramElement(0, Generic_formatDirection(Direction(3)))

    @staticmethod
    def direction_lr() -> ClassDiagramElement:
        return ClassDiagramElement(0, Generic_formatDirection(Direction(4)))

    @staticmethod
    def click_href(id: str, url: str, tooltip: str | None=None) -> ClassDiagramElement:
        return ClassDiagramElement(0, Generic_formatClickHref(id, url, tooltip))

    @staticmethod
    def note(txt: str, id: str | None=None) -> ClassDiagramElement:
        return ClassDiagramElement(0, ClassDiagram_formatNote(txt, id))

    @staticmethod
    def link(id: str, url: str, tooltip: str | None=None) -> ClassDiagramElement:
        return ClassDiagramElement(0, Generic_formatClickHref(id, url, tooltip))

    @staticmethod
    def style(id: str, styles: Any) -> ClassDiagramElement:
        return ClassDiagramElement(0, ClassDiagram_formatClassStyles(id, of_seq(styles)))

    @staticmethod
    def css_class(ids: Any, class_name: str) -> ClassDiagramElement:
        return ClassDiagramElement(0, ClassDiagram_formatCssClass(of_seq(ids), class_name))


classDiagram_reflection = _expr173

def _expr178() -> TypeInfo:
    return class_type("Siren.state_diagram", None, state_diagram)


class state_diagram:
    @staticmethod
    def state(id: str, description: str | None=None) -> StateDiagramElement:
        return StateDiagramElement(0, StateDiagram_formatState(id, description))

    @staticmethod
    def transition(id1: str, id2: str, description: str | None=None) -> StateDiagramElement:
        return StateDiagramElement(0, StateDiagram_formatTransition(id1, id2, description))

    @staticmethod
    def transition_start(id: str, description: str | None=None) -> StateDiagramElement:
        return StateDiagramElement(0, StateDiagram_formatTransition(state_diagram.start_end(), id, description))

    @staticmethod
    def transition_end(id: str, description: str | None=None) -> StateDiagramElement:
        return StateDiagramElement(0, StateDiagram_formatTransition(id, state_diagram.start_end(), description))

    @staticmethod
    def start_end() -> str:
        return "[*]"

    @staticmethod
    def state_composite(id: str, children: Any) -> StateDiagramElement:
        return StateDiagramElement(1, to_text(printf("state %s {"))(id), "}", of_seq(children))

    @staticmethod
    def state_choice(id: str) -> StateDiagramElement:
        return StateDiagramElement(0, to_text(printf("state %s <<choice>>"))(id))

    @staticmethod
    def state_fork(id: str) -> StateDiagramElement:
        return StateDiagramElement(0, to_text(printf("state %s <<fork>>"))(id))

    @staticmethod
    def state_join(id: str) -> StateDiagramElement:
        return StateDiagramElement(0, to_text(printf("state %s <<join>>"))(id))

    @staticmethod
    def note(id: str, msg: str, note_position: NotePosition | None=None) -> StateDiagramElement:
        if equals(value_1(note_position), NotePosition(0)) if (note_position is not None) else False:
            raise Exception("Error: Cannot use \"over\" for note in State Diagram!")

        lines: Array[str] = split(msg, ["\r\n", "\n"], None, 1)
        def _arrow175(__unit: None=None) -> IEnumerable_1[StateDiagramElement]:
            def _arrow174(line: str) -> StateDiagramElement:
                return StateDiagramElement(0, line)

            return map_1(_arrow174, lines)

        return StateDiagramElement(1, StateDiagram_formatNoteWrapper(id, note_position), "end note", to_list(delay(_arrow175)))

    @staticmethod
    def note_multi_line(id: str, lines: Any, note_position: NotePosition | None=None) -> StateDiagramElement:
        if equals(value_1(note_position), NotePosition(0)) if (note_position is not None) else False:
            raise Exception("Error: Cannot use \"over\" for note in State Diagram!")

        def _arrow177(__unit: None=None) -> IEnumerable_1[StateDiagramElement]:
            def _arrow176(line: str) -> StateDiagramElement:
                return StateDiagramElement(0, line)

            return map_1(_arrow176, lines)

        return StateDiagramElement(1, StateDiagram_formatNoteWrapper(id, note_position), "end note", to_list(delay(_arrow177)))

    @staticmethod
    def note_line(id: str, msg: str, note_position: NotePosition | None=None) -> StateDiagramElement:
        if equals(value_1(note_position), NotePosition(0)) if (note_position is not None) else False:
            raise Exception("Error: Cannot use \"over\" for note in State Diagram!")

        return StateDiagramElement(0, Generic_formatNote(id, note_position, msg))

    @staticmethod
    def concurrency() -> StateDiagramElement:
        return StateDiagramElement(0, "--")

    @staticmethod
    def direction(direction_1: Direction) -> StateDiagramElement:
        return StateDiagramElement(0, Generic_formatDirection(direction_1))

    @staticmethod
    def comment(txt: str) -> StateDiagramElement:
        return StateDiagramElement(0, Generic_formatComment(txt))

    @staticmethod
    def class_def(class_name: str, styles: Any) -> StateDiagramElement:
        return StateDiagramElement(0, Generic_formatClassDef(class_name, of_seq(styles)))

    @staticmethod
    def class_(node_ids: Any, class_name: str) -> StateDiagramElement:
        return StateDiagramElement(0, Generic_formatClass(of_seq(node_ids), class_name))


state_diagram_reflection = _expr178

def _expr179() -> TypeInfo:
    return class_type("Siren.erKey", None, erKey)


class er_key:
    @staticmethod
    def pk() -> ERKeyType:
        return ERKeyType(0)

    @staticmethod
    def fk() -> ERKeyType:
        return ERKeyType(1)

    @staticmethod
    def uk() -> ERKeyType:
        return ERKeyType(2)


erKey_reflection = _expr179

def _expr180() -> TypeInfo:
    return class_type("Siren.erCardinality", None, erCardinality)


class er_cardinality:
    @staticmethod
    def one_or_many() -> ERCardinalityType:
        return ERCardinalityType(1)

    @staticmethod
    def one_or_zero() -> ERCardinalityType:
        return ERCardinalityType(0)

    @staticmethod
    def only_one() -> ERCardinalityType:
        return ERCardinalityType(3)

    @staticmethod
    def zero_or_many() -> ERCardinalityType:
        return ERCardinalityType(2)


erCardinality_reflection = _expr180

def _expr185() -> TypeInfo:
    return class_type("Siren.erDiagram", None, erDiagram)


class er_diagram:
    @staticmethod
    def raw(line: str) -> ERDiagramElement:
        return ERDiagramElement(0, line)

    @staticmethod
    def entity(id: str, attr: Any | None=None) -> ERDiagramElement:
        if attr is not None:
            def _arrow182(__unit: None=None) -> IEnumerable_1[ERDiagramElement]:
                def _arrow181(attr_1: ERAttribute) -> ERDiagramElement:
                    return ERDiagramElement(0, ERDiagram_formatAttribute(attr_1))

                return map_1(_arrow181, value_1(attr))

            children: FSharpList[ERDiagramElement] = to_list(delay(_arrow182))
            return ERDiagramElement(1, ERDiagram_formatEntityWrapper(id, None), "}", children)

        else: 
            return ERDiagramElement(0, ERDiagram_formatEntityNode(id, None))


    @staticmethod
    def entity_alias(id: str, alias: str, attr: Any | None=None) -> ERDiagramElement:
        if attr is not None:
            def _arrow184(__unit: None=None) -> IEnumerable_1[ERDiagramElement]:
                def _arrow183(attr_1: ERAttribute) -> ERDiagramElement:
                    return ERDiagramElement(0, ERDiagram_formatAttribute(attr_1))

                return map_1(_arrow183, value_1(attr))

            children: FSharpList[ERDiagramElement] = to_list(delay(_arrow184))
            return ERDiagramElement(1, ERDiagram_formatEntityWrapper(id, alias), "}", children)

        else: 
            return ERDiagramElement(0, ERDiagram_formatEntityNode(id, alias))


    @staticmethod
    def relationship(id1: str, er_cardinality1: ERCardinalityType, id2: str, er_cardinality2: ERCardinalityType, message: str, is_optional: bool | None=None) -> ERDiagramElement:
        return ERDiagramElement(0, ERDiagram_formatRelationship(id1, er_cardinality1, id2, er_cardinality2, message, is_optional))

    @staticmethod
    def attribute(attr_type: str, name: str, keys: Any | None=None, comment: str | None=None) -> ERAttribute:
        return ERAttribute(attr_type, name, default_arg(map_2(of_seq, keys), empty_1()), comment)


erDiagram_reflection = _expr185

def _expr186() -> TypeInfo:
    return class_type("Siren.journey", None, journey)


class journey:
    @staticmethod
    def raw(line: str) -> JourneyElement:
        return JourneyElement(0, line)

    @staticmethod
    def title(name: str) -> JourneyElement:
        return JourneyElement(0, to_text(printf("title %s"))(name))

    @staticmethod
    def section(name: str) -> JourneyElement:
        return JourneyElement(0, to_text(printf("section %s"))(name))

    @staticmethod
    def task(name: str, score: int, actors: Any) -> JourneyElement:
        return JourneyElement(0, UserJourney_formatTask(name, score, some(actors)))

    @staticmethod
    def task_empty(name: str, score: int) -> JourneyElement:
        return JourneyElement(0, UserJourney_formatTask(name, score, None))


journey_reflection = _expr186

def _expr187() -> TypeInfo:
    return class_type("Siren.ganttTime", None, ganttTime)


class gantt_time:
    @staticmethod
    def length(timespan: str) -> str:
        return timespan

    @staticmethod
    def date_time(datetime: str) -> str:
        return datetime

    @staticmethod
    def after(id: str) -> str:
        return to_text(printf("after %s"))(id)

    @staticmethod
    def until(id: str) -> str:
        return to_text(printf("until %s"))(id)


ganttTime_reflection = _expr187

def _expr188() -> TypeInfo:
    return class_type("Siren.gantt_tags", None, gantt_tags)


class gantt_tags:
    @staticmethod
    def active() -> GanttTags:
        return GanttTags(0)

    @staticmethod
    def done() -> GanttTags:
        return GanttTags(1)

    @staticmethod
    def crit() -> GanttTags:
        return GanttTags(2)

    @staticmethod
    def milestone() -> GanttTags:
        return GanttTags(3)


gantt_tags_reflection = _expr188

def _expr189() -> TypeInfo:
    return class_type("Siren.ganttUnit", None, ganttUnit)


class gantt_unit:
    @staticmethod
    def millisecond() -> GanttUnit:
        return GanttUnit(0)

    @staticmethod
    def second() -> GanttUnit:
        return GanttUnit(1)

    @staticmethod
    def minute() -> GanttUnit:
        return GanttUnit(2)

    @staticmethod
    def hour() -> GanttUnit:
        return GanttUnit(3)

    @staticmethod
    def day() -> GanttUnit:
        return GanttUnit(4)

    @staticmethod
    def week() -> GanttUnit:
        return GanttUnit(5)

    @staticmethod
    def month() -> GanttUnit:
        return GanttUnit(6)


ganttUnit_reflection = _expr189

def _expr191() -> TypeInfo:
    return class_type("Siren.gantt", None, gantt)


class gantt:
    @staticmethod
    def raw(line: str) -> GanttElement:
        return GanttElement(0, line)

    @staticmethod
    def title(name: str) -> GanttElement:
        return GanttElement(0, to_text(printf("title %s"))(name))

    @staticmethod
    def section(name: str) -> GanttElement:
        return GanttElement(0, to_text(printf("section %s"))(name))

    @staticmethod
    def task(title: str, id: str, start_date: str, end_date: str, tags: Any | None=None) -> GanttElement:
        return GanttElement(0, Gantt_formatTask(title, Option_defaultBind(of_seq, empty_1(), tags), id, start_date, end_date))

    @staticmethod
    def task_start_end(title: str, start_date: str, end_date: str, tags: Any | None=None) -> GanttElement:
        return GanttElement(0, Gantt_formatTask(title, Option_defaultBind(of_seq, empty_1(), tags), None, start_date, end_date))

    @staticmethod
    def task_end(title: str, end_date: str, tags: Any | None=None) -> GanttElement:
        return GanttElement(0, Gantt_formatTask(title, Option_defaultBind(of_seq, empty_1(), tags), None, None, end_date))

    @staticmethod
    def milestone(title: str, id: str, start_date: str, end_date: str, tags: Any | None=None) -> GanttElement:
        return GanttElement(0, Gantt_formatTask(title, cons(gantt_tags.milestone(), Option_defaultBind(of_seq, empty_1(), tags)), id, start_date, end_date))

    @staticmethod
    def milestone_start_end(title: str, start_date: str, end_date: str, tags: Any | None=None) -> GanttElement:
        return GanttElement(0, Gantt_formatTask(title, cons(gantt_tags.milestone(), Option_defaultBind(of_seq, empty_1(), tags)), None, start_date, end_date))

    @staticmethod
    def milestone_end(title: str, end_date: str, tags: Any | None=None) -> GanttElement:
        return GanttElement(0, Gantt_formatTask(title, cons(gantt_tags.milestone(), Option_defaultBind(of_seq, empty_1(), tags)), None, None, end_date))

    @staticmethod
    def date_format(format_string: str) -> GanttElement:
        return GanttElement(0, to_text(printf("dateFormat %s"))(format_string))

    @staticmethod
    def axis_format(format_string: str) -> GanttElement:
        return GanttElement(0, to_text(printf("axisFormat %s"))(format_string))

    @staticmethod
    def tick_interval(interval: int, unit: GanttUnit) -> GanttElement:
        def _arrow190(__unit: None=None) -> str:
            arg_1: str = Siren_GanttUnit__GanttUnit_ToFormatString(unit)
            return to_text(printf("tickInterval %i%s"))(interval)(arg_1)

        return GanttElement(0, _arrow190())

    @staticmethod
    def weekday(day: str) -> GanttElement:
        return GanttElement(0, to_text(printf("weekday %s"))(day))

    @staticmethod
    def excludes(day: str) -> GanttElement:
        return GanttElement(0, to_text(printf("excludes %s"))(day))

    @staticmethod
    def comment(txt: str) -> GanttElement:
        return GanttElement(0, Generic_formatComment(txt))


gantt_reflection = _expr191

def _expr192() -> TypeInfo:
    return class_type("Siren.pieChart", None, pieChart)


class pie_chart:
    @staticmethod
    def raw(line: str) -> PieChartElement:
        return PieChartElement(0, line)

    @staticmethod
    def data(name: str, value: float) -> PieChartElement:
        return PieChartElement(0, PieChart_formatData(name, value))


pieChart_reflection = _expr192

def _expr193() -> TypeInfo:
    return class_type("Siren.quadrant", None, quadrant)


class quadrant:
    @staticmethod
    def raw(txt: str) -> QuadrantElement:
        return QuadrantElement(0, txt)

    @staticmethod
    def title(title: str) -> QuadrantElement:
        return QuadrantElement(0, "title " + title)

    @staticmethod
    def x_axis(left: str, right: str | None=None) -> QuadrantElement:
        return QuadrantElement(0, QuadrantChart_formatXAxis(left, right))

    @staticmethod
    def y_axis(bottom: str, top: str | None=None) -> QuadrantElement:
        return QuadrantElement(0, QuadrantChart_formatYAxis(bottom, top))

    @staticmethod
    def quadrant1(title: str) -> QuadrantElement:
        return QuadrantElement(0, "quadrant-1 " + title)

    @staticmethod
    def quadrant2(title: str) -> QuadrantElement:
        return QuadrantElement(0, "quadrant-2 " + title)

    @staticmethod
    def quadrant3(title: str) -> QuadrantElement:
        return QuadrantElement(0, "quadrant-3 " + title)

    @staticmethod
    def quadrant4(title: str) -> QuadrantElement:
        return QuadrantElement(0, "quadrant-4 " + title)

    @staticmethod
    def point(name: str, x_axis: float, y_axis: float) -> QuadrantElement:
        return QuadrantElement(0, QuadrantChart_formatPoint(name, x_axis, y_axis))

    @staticmethod
    def comment(txt: str) -> QuadrantElement:
        return QuadrantElement(0, Generic_formatComment(txt))


quadrant_reflection = _expr193

def _expr194() -> TypeInfo:
    return class_type("Siren.rqRisk", None, rqRisk)


class rq_risk:
    @staticmethod
    def low() -> RDRiskType:
        return RDRiskType(0)

    @staticmethod
    def medium() -> RDRiskType:
        return RDRiskType(1)

    @staticmethod
    def high() -> RDRiskType:
        return RDRiskType(2)


rqRisk_reflection = _expr194

def _expr195() -> TypeInfo:
    return class_type("Siren.rqMethod", None, rqMethod)


class rq_method:
    @staticmethod
    def analysis() -> RDVerifyMethod:
        return RDVerifyMethod(0)

    @staticmethod
    def inspection() -> RDVerifyMethod:
        return RDVerifyMethod(1)

    @staticmethod
    def test() -> RDVerifyMethod:
        return RDVerifyMethod(2)

    @staticmethod
    def demonstration() -> RDVerifyMethod:
        return RDVerifyMethod(3)


rqMethod_reflection = _expr195

def _expr196() -> TypeInfo:
    return class_type("Siren.requirement", None, requirement)


class requirement:
    @staticmethod
    def raw(txt: str) -> RequirementDiagramElement:
        return RequirementDiagramElement(0, txt)

    @staticmethod
    def requirement(name: str, id: str | None=None, text: str | None=None, rq_risk: RDRiskType | None=None, rq_method: RDVerifyMethod | None=None) -> RequirementDiagramElement:
        return RequirementDiagram_createRequirement("requirement", name, id, text, rq_risk, rq_method)

    @staticmethod
    def functional_requirement(name: str, id: str | None=None, text: str | None=None, rq_risk: RDRiskType | None=None, rq_method: RDVerifyMethod | None=None) -> RequirementDiagramElement:
        return RequirementDiagram_createRequirement("functionalRequirement", name, id, text, rq_risk, rq_method)

    @staticmethod
    def interface_requirement(name: str, id: str | None=None, text: str | None=None, rq_risk: RDRiskType | None=None, rq_method: RDVerifyMethod | None=None) -> RequirementDiagramElement:
        return RequirementDiagram_createRequirement("interfaceRequirement", name, id, text, rq_risk, rq_method)

    @staticmethod
    def performance_requirement(name: str, id: str | None=None, text: str | None=None, rq_risk: RDRiskType | None=None, rq_method: RDVerifyMethod | None=None) -> RequirementDiagramElement:
        return RequirementDiagram_createRequirement("performanceRequirement", name, id, text, rq_risk, rq_method)

    @staticmethod
    def physical_requirement(name: str, id: str | None=None, text: str | None=None, rq_risk: RDRiskType | None=None, rq_method: RDVerifyMethod | None=None) -> RequirementDiagramElement:
        return RequirementDiagram_createRequirement("physicalRequirement", name, id, text, rq_risk, rq_method)

    @staticmethod
    def design_constraint(name: str, id: str | None=None, text: str | None=None, rq_risk: RDRiskType | None=None, rq_method: RDVerifyMethod | None=None) -> RequirementDiagramElement:
        return RequirementDiagram_createRequirement("designConstraint", name, id, text, rq_risk, rq_method)

    @staticmethod
    def element(name: str, element_type: str | None=None, docref: str | None=None) -> RequirementDiagramElement:
        return RequirementDiagram_createElement(name, element_type, docref)

    @staticmethod
    def contains(id1: str, id2: str) -> RequirementDiagramElement:
        return RequirementDiagramElement(0, RequirementDiagram_formatRelationship(id1, id2, RDRelationship(0)))

    @staticmethod
    def copies(id1: str, id2: str) -> RequirementDiagramElement:
        return RequirementDiagramElement(0, RequirementDiagram_formatRelationship(id1, id2, RDRelationship(1)))

    @staticmethod
    def derives(id1: str, id2: str) -> RequirementDiagramElement:
        return RequirementDiagramElement(0, RequirementDiagram_formatRelationship(id1, id2, RDRelationship(2)))

    @staticmethod
    def satisfies(id1: str, id2: str) -> RequirementDiagramElement:
        return RequirementDiagramElement(0, RequirementDiagram_formatRelationship(id1, id2, RDRelationship(3)))

    @staticmethod
    def verifies(id1: str, id2: str) -> RequirementDiagramElement:
        return RequirementDiagramElement(0, RequirementDiagram_formatRelationship(id1, id2, RDRelationship(4)))

    @staticmethod
    def refines(id1: str, id2: str) -> RequirementDiagramElement:
        return RequirementDiagramElement(0, RequirementDiagram_formatRelationship(id1, id2, RDRelationship(5)))

    @staticmethod
    def traces(id1: str, id2: str) -> RequirementDiagramElement:
        return RequirementDiagramElement(0, RequirementDiagram_formatRelationship(id1, id2, RDRelationship(6)))


requirement_reflection = _expr196

def _expr197() -> TypeInfo:
    return class_type("Siren.gitType", None, gitType)


class git_type:
    @staticmethod
    def normal() -> GitCommitType:
        return GitCommitType(0)

    @staticmethod
    def reverse() -> GitCommitType:
        return GitCommitType(1)

    @staticmethod
    def highlight() -> GitCommitType:
        return GitCommitType(2)


gitType_reflection = _expr197

def _expr198() -> TypeInfo:
    return class_type("Siren.git", None, git)


class git:
    @staticmethod
    def raw(line: str) -> GitGraphElement:
        return GitGraphElement(0, line)

    @staticmethod
    def commit(id: str | None=None, git_type: GitCommitType | None=None, tag: str | None=None) -> GitGraphElement:
        return GitGraphElement(0, Git_formatCommit(id, git_type, tag))

    @staticmethod
    def merge(target_branch_id: str, mergeid: str | None=None, git_type: GitCommitType | None=None, tag: str | None=None) -> GitGraphElement:
        return GitGraphElement(0, Git_formatMerge(target_branch_id, mergeid, git_type, tag))

    @staticmethod
    def cherry_pick(commitid: str, parent_id: str | None=None) -> GitGraphElement:
        return GitGraphElement(0, Git_formatCherryPick(commitid, parent_id))

    @staticmethod
    def branch(id: str) -> GitGraphElement:
        return GitGraphElement(0, "branch " + id)

    @staticmethod
    def checkout(id: str) -> GitGraphElement:
        return GitGraphElement(0, "checkout " + id)


git_reflection = _expr198

def _expr200() -> TypeInfo:
    return class_type("Siren.mindmap", None, mindmap)


class mindmap:
    @staticmethod
    def raw(line: str) -> MindmapElement:
        return MindmapElement(0, line)

    @staticmethod
    def node(name: str, children: Any | None=None) -> MindmapElement:
        return Mindmap_handleNodeChildren(children, name)

    @staticmethod
    def square(name: str, children: Any | None=None) -> MindmapElement:
        return Mindmap_handleNodeChildren(children, Mindmap_formatNode(name, None, MindmapShape(0)))

    @staticmethod
    def square_id(id: str, name: str, children: Any | None=None) -> MindmapElement:
        return Mindmap_handleNodeChildren(children, Mindmap_formatNode(id, name, MindmapShape(0)))

    @staticmethod
    def rounded_square(name: str, children: Any | None=None) -> MindmapElement:
        return Mindmap_handleNodeChildren(children, Mindmap_formatNode(name, None, MindmapShape(1)))

    @staticmethod
    def rounded_square_id(id: str, name: str, children: Any | None=None) -> MindmapElement:
        return Mindmap_handleNodeChildren(children, Mindmap_formatNode(id, name, MindmapShape(1)))

    @staticmethod
    def circle(name: str, children: Any | None=None) -> MindmapElement:
        return Mindmap_handleNodeChildren(children, Mindmap_formatNode(name, None, MindmapShape(2)))

    @staticmethod
    def circle_id(id: str, name: str, children: Any | None=None) -> MindmapElement:
        return Mindmap_handleNodeChildren(children, Mindmap_formatNode(id, name, MindmapShape(2)))

    @staticmethod
    def bang(name: str, children: Any | None=None) -> MindmapElement:
        return Mindmap_handleNodeChildren(children, Mindmap_formatNode(name, None, MindmapShape(3)))

    @staticmethod
    def bang_id(id: str, name: str, children: Any | None=None) -> MindmapElement:
        return Mindmap_handleNodeChildren(children, Mindmap_formatNode(id, name, MindmapShape(3)))

    @staticmethod
    def cloud(name: str, children: Any | None=None) -> MindmapElement:
        return Mindmap_handleNodeChildren(children, Mindmap_formatNode(name, None, MindmapShape(4)))

    @staticmethod
    def cloud_id(id: str, name: str, children: Any | None=None) -> MindmapElement:
        return Mindmap_handleNodeChildren(children, Mindmap_formatNode(id, name, MindmapShape(4)))

    @staticmethod
    def hexagon(name: str, children: Any | None=None) -> MindmapElement:
        return Mindmap_handleNodeChildren(children, Mindmap_formatNode(name, None, MindmapShape(5)))

    @staticmethod
    def hexagon_id(id: str, name: str, children: Any | None=None) -> MindmapElement:
        return Mindmap_handleNodeChildren(children, Mindmap_formatNode(id, name, MindmapShape(5)))

    @staticmethod
    def icon(icon_class: str) -> MindmapElement:
        return MindmapElement(0, to_text(printf("::icon(%s)"))(icon_class))

    @staticmethod
    def class_name(class_name: str) -> MindmapElement:
        return MindmapElement(0, to_text(printf("::: %s"))(class_name))

    @staticmethod
    def class_names(class_names: Any | None=None) -> MindmapElement:
        def _arrow199(__unit: None=None) -> str:
            arg: str = join(" ", class_names)
            return to_text(printf("::: %s"))(arg)

        return MindmapElement(0, _arrow199())

    @staticmethod
    def comment(txt: str) -> str:
        return Generic_formatComment(txt)


mindmap_reflection = _expr200

def _expr201() -> TypeInfo:
    return class_type("Siren.timeline", None, timeline)


class timeline:
    @staticmethod
    def raw(line: str) -> TimelineElement:
        return TimelineElement(0, line)

    @staticmethod
    def title(name: str) -> TimelineElement:
        return TimelineElement(0, "title " + name)

    @staticmethod
    def period(name: str) -> TimelineElement:
        return TimelineElement(0, name)

    @staticmethod
    def single(time_period: str, event: str | None=None) -> TimelineElement:
        return TimelineElement(0, Timeline_formatSingle(time_period, event))

    @staticmethod
    def multiple(time_period: str, events: Any) -> TimelineElement:
        return Timeline_createMultiple(time_period, of_seq(events))

    @staticmethod
    def section(name: str, children: Any) -> TimelineElement:
        return TimelineElement(1, "section " + name, "", of_seq(children))

    @staticmethod
    def comment(txt: str) -> TimelineElement:
        return TimelineElement(0, Generic_formatComment(txt))


timeline_reflection = _expr201

def _expr202() -> TypeInfo:
    return class_type("Siren.sankey", None, sankey)


class sankey:
    @staticmethod
    def raw(line: str) -> SankeyElement:
        return SankeyElement(0, line)

    @staticmethod
    def comment(txt: str) -> SankeyElement:
        return SankeyElement(0, Generic_formatComment(txt))

    @staticmethod
    def link(source: str, target: str, value: float) -> SankeyElement:
        return SankeyElement(0, Sankey_formatLink(source, target, value))

    @staticmethod
    def links(source: str, targets: Any) -> SankeyElement:
        return Sankey_createLinks(source, of_seq(targets))


sankey_reflection = _expr202

def _expr203() -> TypeInfo:
    return class_type("Siren.xyChart", None, xyChart)


class xy_chart:
    @staticmethod
    def raw(line: str) -> XYChartElement:
        return XYChartElement(0, line)

    @staticmethod
    def title(name: str) -> XYChartElement:
        return XYChartElement(0, to_text(printf("title \"%s\""))(name))

    @staticmethod
    def x_axis(data: Any | None=None) -> XYChartElement:
        return XYChartElement(0, XYChart_formatXAxis(None, of_seq(data)))

    @staticmethod
    def x_axis_named(name: str, data: Any) -> XYChartElement:
        return XYChartElement(0, XYChart_formatXAxis(name, of_seq(data)))

    @staticmethod
    def x_axis_range(range_start: float, range_end: float) -> XYChartElement:
        return XYChartElement(0, XYChart_formatXAxisRange(None, range_start, range_end))

    @staticmethod
    def x_axis_named_range(name: str, range_start: float, range_end: float) -> XYChartElement:
        return XYChartElement(0, XYChart_formatXAxisRange(name, range_start, range_end))

    @staticmethod
    def y_axis(name: str) -> XYChartElement:
        return XYChartElement(0, XYChart_formatYAxis(name, None))

    @staticmethod
    def y_axis_range(range_start: float, range_end: float) -> XYChartElement:
        return XYChartElement(0, XYChart_formatYAxis(None, (range_start, range_end)))

    @staticmethod
    def y_axis_named_range(name: str, range_start: float, range_end: float) -> XYChartElement:
        return XYChartElement(0, XYChart_formatYAxis(name, (range_start, range_end)))

    @staticmethod
    def line(data: Any | None=None) -> XYChartElement:
        return XYChartElement(0, XYChart_formatLine(of_seq(data)))

    @staticmethod
    def bar(data: Any | None=None) -> XYChartElement:
        return XYChartElement(0, XYChart_formatBar(of_seq(data)))

    @staticmethod
    def comment(txt: str) -> XYChartElement:
        return XYChartElement(0, Generic_formatComment(txt))


xyChart_reflection = _expr203

def _expr204() -> TypeInfo:
    return class_type("Siren.block", None, block)


class block:
    @staticmethod
    def columns(count: int) -> BlockElement:
        return BlockElement(0, to_text(printf("columns %i"))(count))

    @staticmethod
    def simple(id: str) -> BlockElement:
        return BlockElement(0, id)

    @staticmethod
    def simples(ids: Any | None=None) -> BlockElement:
        return BlockElement(0, join(" ", ids))

    @staticmethod
    def c_block(children: Any | None=None) -> BlockElement:
        return BlockElement(1, "block", "end", of_seq(children))

    @staticmethod
    def c_id_block(id: str, children: Any) -> BlockElement:
        return BlockElement(1, to_text(printf("block:%s"))(id), "end", of_seq(children))

    @staticmethod
    def c_id_width_block(id: str, width: int, children: Any) -> BlockElement:
        return BlockElement(1, to_text(printf("block:%s:%i"))(id)(width), "end", of_seq(children))

    @staticmethod
    def line(children: Any | None=None) -> BlockElement:
        return BlockElement(2, of_seq(children))

    @staticmethod
    def block(id: str, label: str | None=None, width: int | None=None) -> BlockElement:
        return BlockElement(0, Block_formatBlockType(id, label, width, BlockBlockType(0)))

    @staticmethod
    def block_rounded(id: str, label: str | None=None, width: int | None=None) -> BlockElement:
        return BlockElement(0, Block_formatBlockType(id, label, width, BlockBlockType(1)))

    @staticmethod
    def block_statidum(id: str, label: str | None=None, width: int | None=None) -> BlockElement:
        return BlockElement(0, Block_formatBlockType(id, label, width, BlockBlockType(2)))

    @staticmethod
    def block_subroutine(id: str, label: str | None=None, width: int | None=None) -> BlockElement:
        return BlockElement(0, Block_formatBlockType(id, label, width, BlockBlockType(3)))

    @staticmethod
    def block_cylindrical(id: str, label: str | None=None, width: int | None=None) -> BlockElement:
        return BlockElement(0, Block_formatBlockType(id, label, width, BlockBlockType(4)))

    @staticmethod
    def block_circle(id: str, label: str | None=None, width: int | None=None) -> BlockElement:
        return BlockElement(0, Block_formatBlockType(id, label, width, BlockBlockType(5)))

    @staticmethod
    def block_asymmetric(id: str, label: str | None=None, width: int | None=None) -> BlockElement:
        return BlockElement(0, Block_formatBlockType(id, label, width, BlockBlockType(6)))

    @staticmethod
    def block_rhombus(id: str, label: str | None=None, width: int | None=None) -> BlockElement:
        return BlockElement(0, Block_formatBlockType(id, label, width, BlockBlockType(7)))

    @staticmethod
    def block_hexagon(id: str, label: str | None=None, width: int | None=None) -> BlockElement:
        return BlockElement(0, Block_formatBlockType(id, label, width, BlockBlockType(8)))

    @staticmethod
    def block_parallelogram(id: str, label: str | None=None, width: int | None=None) -> BlockElement:
        return BlockElement(0, Block_formatBlockType(id, label, width, BlockBlockType(9)))

    @staticmethod
    def block_parallelogram_alt(id: str, label: str | None=None, width: int | None=None) -> BlockElement:
        return BlockElement(0, Block_formatBlockType(id, label, width, BlockBlockType(10)))

    @staticmethod
    def block_trapezoid(id: str, label: str | None=None, width: int | None=None) -> BlockElement:
        return BlockElement(0, Block_formatBlockType(id, label, width, BlockBlockType(11)))

    @staticmethod
    def block_trapezoid_alt(id: str, label: str | None=None, width: int | None=None) -> BlockElement:
        return BlockElement(0, Block_formatBlockType(id, label, width, BlockBlockType(12)))

    @staticmethod
    def block_double_circle(id: str, label: str | None=None, width: int | None=None) -> BlockElement:
        return BlockElement(0, Block_formatBlockType(id, label, width, BlockBlockType(13)))

    @staticmethod
    def arrow_right_labeled(id: str, label: str | None=None) -> BlockElement:
        return BlockElement(0, Block_formatBlockArrow(id, label, BlockArrowDirection(0)))

    @staticmethod
    def arrow_right(id: str, width: int | None=None) -> BlockElement:
        return BlockElement(0, Block_formatEmptyBlockArrow(id, width, BlockArrowDirection(0)))

    @staticmethod
    def arrow_left_labeled(id: str, label: str | None=None) -> BlockElement:
        return BlockElement(0, Block_formatBlockArrow(id, label, BlockArrowDirection(1)))

    @staticmethod
    def arrow_left(id: str, width: int | None=None) -> BlockElement:
        return BlockElement(0, Block_formatEmptyBlockArrow(id, width, BlockArrowDirection(1)))

    @staticmethod
    def arrow_up_labeled(id: str, label: str | None=None) -> BlockElement:
        return BlockElement(0, Block_formatBlockArrow(id, label, BlockArrowDirection(2)))

    @staticmethod
    def arrow_up(id: str, width: int | None=None) -> BlockElement:
        return BlockElement(0, Block_formatEmptyBlockArrow(id, width, BlockArrowDirection(2)))

    @staticmethod
    def arrow_down_labeled(id: str, label: str | None=None) -> BlockElement:
        return BlockElement(0, Block_formatBlockArrow(id, label, BlockArrowDirection(3)))

    @staticmethod
    def arrow_down(id: str, width: int | None=None) -> BlockElement:
        return BlockElement(0, Block_formatEmptyBlockArrow(id, width, BlockArrowDirection(3)))

    @staticmethod
    def arrow_xlabeled(id: str, label: str | None=None) -> BlockElement:
        return BlockElement(0, Block_formatBlockArrow(id, label, BlockArrowDirection(4)))

    @staticmethod
    def arrow_x(id: str, width: int | None=None) -> BlockElement:
        return BlockElement(0, Block_formatEmptyBlockArrow(id, width, BlockArrowDirection(4)))

    @staticmethod
    def arrow_ylabeled(id: str, label: str | None=None) -> BlockElement:
        return BlockElement(0, Block_formatBlockArrow(id, label, BlockArrowDirection(5)))

    @staticmethod
    def arrow_y(id: str, width: int | None=None) -> BlockElement:
        return BlockElement(0, Block_formatEmptyBlockArrow(id, width, BlockArrowDirection(5)))

    @staticmethod
    def arrow_custom_labeled(id: str, direction_1: str, label: str | None=None) -> BlockElement:
        return BlockElement(0, Block_formatBlockArrow(id, label, BlockArrowDirection(6, direction_1)))

    @staticmethod
    def arrow_custom(id: str, direction_1: str, width: int | None=None) -> BlockElement:
        return BlockElement(0, Block_formatEmptyBlockArrow(id, width, BlockArrowDirection(6, direction_1)))

    @staticmethod
    def space() -> BlockElement:
        return BlockElement(0, Block_formatSpace(None))

    @staticmethod
    def spacew(width: int | None=None) -> BlockElement:
        return BlockElement(0, Block_formatSpace(width))

    @staticmethod
    def link(id1: str, id2: str, label: str | None=None) -> BlockElement:
        return BlockElement(0, Block_formatLink(id1, id2, label))

    @staticmethod
    def style(id: str, styles: Any) -> BlockElement:
        return BlockElement(0, Block_formatStyle(id, of_seq(styles)))

    @staticmethod
    def class_def(class_name: str, styles: Any) -> BlockElement:
        return BlockElement(0, Generic_formatClassDef(class_name, of_seq(styles)))

    @staticmethod
    def class_(node_ids: Any, class_name: str) -> BlockElement:
        return BlockElement(0, Block_formatClass(of_seq(node_ids), class_name))

    @staticmethod
    def comment(txt: str) -> BlockElement:
        return BlockElement(0, Generic_formatComment(txt))


block_reflection = _expr204

def _expr205() -> TypeInfo:
    return class_type("Siren.theme", None, theme)


class theme:
    @staticmethod
    def light() -> str:
        return "default"

    @staticmethod
    def neutral() -> str:
        return "neutral"

    @staticmethod
    def dark() -> str:
        return "dark"

    @staticmethod
    def forest() -> str:
        return "forest"

    @staticmethod
    def base() -> str:
        return "base"

    @staticmethod
    def custom(theme_1: str) -> str:
        return theme_1


theme_reflection = _expr205

def _expr206() -> TypeInfo:
    return class_type("Siren.siren", None, siren)


class siren:
    @staticmethod
    def flowchart(direction_1: Direction, children: Any) -> SirenElement:
        graph: SirenGraph = SirenGraph(0, direction_1, of_seq(children))
        return SirenElement.init(graph)

    @staticmethod
    def sequence(children: Any | None=None) -> SirenElement:
        graph: SirenGraph = SirenGraph(1, of_seq(children))
        return SirenElement.init(graph)

    @staticmethod
    def class_diagram(children: Any | None=None) -> SirenElement:
        graph: SirenGraph = SirenGraph(2, of_seq(children))
        return SirenElement.init(graph)

    @staticmethod
    def state(children: Any | None=None) -> SirenElement:
        graph: SirenGraph = SirenGraph(3, of_seq(children))
        return SirenElement.init(graph)

    @staticmethod
    def state_v2(children: Any | None=None) -> SirenElement:
        graph: SirenGraph = SirenGraph(4, of_seq(children))
        return SirenElement.init(graph)

    @staticmethod
    def er_diagram(children: Any | None=None) -> SirenElement:
        graph: SirenGraph = SirenGraph(5, of_seq(children))
        return SirenElement.init(graph)

    @staticmethod
    def journey(children: Any | None=None) -> SirenElement:
        graph: SirenGraph = SirenGraph(6, of_seq(children))
        return SirenElement.init(graph)

    @staticmethod
    def gantt(children: Any | None=None) -> SirenElement:
        graph: SirenGraph = SirenGraph(7, of_seq(children))
        return SirenElement.init(graph)

    @staticmethod
    def pie_chart(children: Any, show_data: bool | None=None, title: str | None=None) -> SirenElement:
        graph: SirenGraph = SirenGraph(8, default_arg(show_data, False), title, of_seq(children))
        return SirenElement.init(graph)

    @staticmethod
    def quadrant(children: Any | None=None) -> SirenElement:
        graph: SirenGraph = SirenGraph(9, of_seq(children))
        return SirenElement.init(graph)

    @staticmethod
    def requirement(children: Any | None=None) -> SirenElement:
        graph: SirenGraph = SirenGraph(10, of_seq(children))
        return SirenElement.init(graph)

    @staticmethod
    def git(children: Any | None=None) -> SirenElement:
        graph: SirenGraph = SirenGraph(11, of_seq(children))
        return SirenElement.init(graph)

    @staticmethod
    def mindmap(children: Any | None=None) -> SirenElement:
        graph: SirenGraph = SirenGraph(12, of_seq(children))
        return SirenElement.init(graph)

    @staticmethod
    def timeline(children: Any | None=None) -> SirenElement:
        graph: SirenGraph = SirenGraph(13, of_seq(children))
        return SirenElement.init(graph)

    @staticmethod
    def sankey(children: Any | None=None) -> SirenElement:
        graph: SirenGraph = SirenGraph(14, of_seq(children))
        return SirenElement.init(graph)

    @staticmethod
    def xy_chart(children: Any, is_horizontal: bool | None=None) -> SirenElement:
        graph: SirenGraph = SirenGraph(15, default_arg(is_horizontal, False), of_seq(children))
        return SirenElement.init(graph)

    @staticmethod
    def block(children: Any | None=None) -> SirenElement:
        graph: SirenGraph = SirenGraph(16, of_seq(children))
        return SirenElement.init(graph)

    @staticmethod
    def with_title(title: str, diagram: SirenElement) -> SirenElement:
        diagram.Config.Title = title
        return diagram

    @staticmethod
    def with_theme(theme_1: str, diagram: SirenElement) -> SirenElement:
        diagram.Config.Theme = theme_1
        return diagram

    @staticmethod
    def with_graph_config(config_func: Callable[[Array[ConfigVariable]], None], diagram: SirenElement) -> SirenElement:
        config: Array[ConfigVariable] = default_arg(diagram.Config.GraphConfig, [])
        config_func(config)
        diagram.Config.GraphConfig = config
        return diagram

    @staticmethod
    def with_theme_variables(theme_variables_func: Callable[[Array[ThemeVariable]], None], diagram: SirenElement) -> SirenElement:
        theme_variables: Array[ThemeVariable] = default_arg(diagram.Config.ThemeVariables, [])
        theme_variables_func(theme_variables)
        diagram.Config.ThemeVariables = theme_variables
        return diagram

    @staticmethod
    def add_theme_variable(var: ThemeVariable, diagram: SirenElement) -> SirenElement:
        diagram.Config.AddThemeVariable(var)
        return diagram

    @staticmethod
    def add_graph_config_variable(var: ConfigVariable, diagram: SirenElement) -> SirenElement:
        diagram.Config.AddGraphConfig(var)
        return diagram

    @staticmethod
    def write(diagram: SirenElement) -> str:
        return Yaml_write(Yaml_root(of_array([diagram.Config.ToYamlAst(), diagram.Graph.ToYamlAst()])))


siren_reflection = _expr206

__all__ = ["formatting_reflection", "direction_reflection", "flowchart_reflection", "notePosition_reflection", "sequence_reflection", "classMemberVisibility_reflection", "classMemberClassifier_reflection", "classDirection_reflection", "classCardinality_reflection", "classRltsType_reflection", "classDiagram_reflection", "state_diagram_reflection", "erKey_reflection", "erCardinality_reflection", "erDiagram_reflection", "journey_reflection", "ganttTime_reflection", "gantt_tags_reflection", "ganttUnit_reflection", "gantt_reflection", "pieChart_reflection", "quadrant_reflection", "rqRisk_reflection", "rqMethod_reflection", "requirement_reflection", "gitType_reflection", "git_reflection", "mindmap_reflection", "timeline_reflection", "sankey_reflection", "xyChart_reflection", "block_reflection", "theme_reflection", "siren_reflection"]

