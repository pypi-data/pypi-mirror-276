from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass
from typing import (Any, TypeVar)
from .fable-library.list import (FSharpList, of_array, singleton as singleton_1, empty as empty_1, fold, map)
from .fable-library.option import (value as value_2, map as map_1, default_arg)
from .fable-library.reflection import (TypeInfo, union_type, string_type, list_type, option_type, record_type, bool_type, class_type)
from .fable-library.seq import (to_list, delay, append, singleton, collect, empty)
from .fable-library.string_ import (join, to_text, printf)
from .fable-library.types import (Array, Union, Record, to_string, seq_to_string)
from .fable-library.util import IEnumerable_1
from .yaml import (Yaml_line, Yaml_level, Yaml_AST, Yaml_root, Yaml_write)

__A = TypeVar("__A")

def YamlHelpers_writeYamlASTBasicWrapper(opener: str, closer: str, children: IEnumerable_1[Any]) -> FSharpList[Yaml_AST]:
    def _arrow7(__unit: None=None, opener: Any=opener, closer: Any=closer, children: Any=children) -> IEnumerable_1[Yaml_AST]:
        def _arrow6(__unit: None=None) -> IEnumerable_1[Yaml_AST]:
            def _arrow4(__unit: None=None) -> IEnumerable_1[Yaml_AST]:
                def _arrow3(child: __A | None=None) -> IEnumerable_1[Yaml_AST]:
                    return child.ToYamlAst()

                return collect(_arrow3, children)

            def _arrow5(__unit: None=None) -> IEnumerable_1[Yaml_AST]:
                return singleton(Yaml_line(closer)) if (closer != "") else empty()

            return append(singleton(Yaml_level(to_list(delay(_arrow4)))), delay(_arrow5))

        return append(singleton(Yaml_line(opener)), delay(_arrow6))

    return to_list(delay(_arrow7))


def YamlHelpers_writeYamlDiagramRoot(opener: str, children: IEnumerable_1[Any]) -> Yaml_AST:
    def _arrow9(__unit: None=None, opener: Any=opener, children: Any=children) -> IEnumerable_1[Yaml_AST]:
        def _arrow8(child: __A | None=None) -> IEnumerable_1[Yaml_AST]:
            return child.ToYamlAst()

        return collect(_arrow8, children)

    return Yaml_root(of_array([Yaml_line(opener), Yaml_level(to_list(delay(_arrow9)))]))


def _expr10() -> TypeInfo:
    return union_type("Siren.NotePosition", [], NotePosition, lambda: [[], [], []])


class NotePosition(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Over", "RightOf", "LeftOf"]


NotePosition_reflection = _expr10

def _expr11() -> TypeInfo:
    return union_type("Siren.Direction", [], Direction, lambda: [[], [], [], [], [], [("Item", string_type)]])


class Direction(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["TB", "TD", "BT", "RL", "LR", "Custom"]

    def __str__(self, __unit: None=None) -> str:
        this: Direction = self
        if this.tag == 1:
            return "TD"

        elif this.tag == 2:
            return "BT"

        elif this.tag == 3:
            return "RL"

        elif this.tag == 4:
            return "LR"

        elif this.tag == 5:
            return this.fields[0]

        else: 
            return "TB"



Direction_reflection = _expr11

def _expr12() -> TypeInfo:
    return union_type("Siren.FlowchartNodeTypes", [], FlowchartNodeTypes, lambda: [[], [], [], [], [], [], [], [], [], [], [], [], [], []])


class FlowchartNodeTypes(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Default", "Round", "Stadium", "Subroutine", "Cylindrical", "Circle", "Asymmetric", "Rhombus", "Hexagon", "Parallelogram", "ParallelogramAlt", "Trapezoid", "TrapezoidAlt", "DoubleCircle"]


FlowchartNodeTypes_reflection = _expr12

def _expr13() -> TypeInfo:
    return union_type("Siren.FlowchartLinkTypes", [], FlowchartLinkTypes, lambda: [[], [], [], [], [], [], [], [], [], [], [], []])


class FlowchartLinkTypes(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Arrow", "Open", "Dotted", "DottedArrow", "Thick", "ThickArrow", "Invisible", "CircleEdge", "CrossEdge", "ArrowDouble", "CircleDouble", "CrossDouble"]


FlowchartLinkTypes_reflection = _expr13

def _expr14() -> TypeInfo:
    return union_type("Siren.SequenceMessageTypes", [], SequenceMessageTypes, lambda: [[], [], [], [], [], [], [], []])


class SequenceMessageTypes(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Solid", "Dotted", "Arrow", "DottedArrow", "CrossEdge", "DottedCrossEdge", "OpenArrow", "DottedOpenArrow"]


SequenceMessageTypes_reflection = _expr14

def _expr15() -> TypeInfo:
    return union_type("Siren.ClassMemberVisibility", [], ClassMemberVisibility, lambda: [[], [], [], [], [("Item", string_type)]])


class ClassMemberVisibility(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Public", "Private", "Protected", "PackageInternal", "Custom"]


ClassMemberVisibility_reflection = _expr15

def _expr16() -> TypeInfo:
    return union_type("Siren.ClassMemberClassifier", [], ClassMemberClassifier, lambda: [[], [], [("Item", string_type)]])


class ClassMemberClassifier(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Abstract", "Static", "Custom"]


ClassMemberClassifier_reflection = _expr16

def _expr17() -> TypeInfo:
    return union_type("Siren.ClassRelationshipDirection", [], ClassRelationshipDirection, lambda: [[], [], []])


class ClassRelationshipDirection(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Left", "Right", "TwoWay"]


ClassRelationshipDirection_reflection = _expr17

def _expr18() -> TypeInfo:
    return union_type("Siren.ClassRelationshipType", [], ClassRelationshipType, lambda: [[], [], [], [], [], [], [], [], []])


class ClassRelationshipType(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Inheritance", "Composition", "Aggregation", "Association", "Link", "Solid", "Dashed", "Dependency", "Realization"]


ClassRelationshipType_reflection = _expr18

def _expr19() -> TypeInfo:
    return union_type("Siren.ClassCardinality", [], ClassCardinality, lambda: [[], [], [], [], [], [], [], [("Item", string_type)]])


class ClassCardinality(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["One", "ZeroOrOne", "OneOrMore", "Many", "N", "ZeroToN", "OneToN", "Custom"]


ClassCardinality_reflection = _expr19

def _expr20() -> TypeInfo:
    return union_type("Siren.ERCardinalityType", [], ERCardinalityType, lambda: [[], [], [], []])


class ERCardinalityType(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["OneOrZero", "OneOrMany", "ZeroOrMany", "OnlyOne"]


ERCardinalityType_reflection = _expr20

def _expr21() -> TypeInfo:
    return union_type("Siren.ERKeyType", [], ERKeyType, lambda: [[], [], []])


class ERKeyType(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["PK", "FK", "UK"]


ERKeyType_reflection = _expr21

def _expr22() -> TypeInfo:
    return record_type("Siren.ERAttribute", [], ERAttribute, lambda: [("Type", string_type), ("Name", string_type), ("Keys", list_type(ERKeyType_reflection())), ("Comment", option_type(string_type))])


@dataclass(eq = False, repr = False, slots = True)
class ERAttribute(Record):
    Type: str
    Name: str
    Keys: FSharpList[ERKeyType]
    Comment: str | None

ERAttribute_reflection = _expr22

def _expr23() -> TypeInfo:
    return union_type("Siren.GanttTags", [], GanttTags, lambda: [[], [], [], []])


class GanttTags(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Active", "Done", "Crit", "Milestone"]


GanttTags_reflection = _expr23

def _expr24() -> TypeInfo:
    return union_type("Siren.GanttUnit", [], GanttUnit, lambda: [[], [], [], [], [], [], []])


class GanttUnit(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Millisecond", "Second", "Minute", "Hour", "Day", "Week", "Month"]


GanttUnit_reflection = _expr24

def _expr25() -> TypeInfo:
    return union_type("Siren.RequirementType", [], RequirementType, lambda: [[], [], [], [], [], []])


class RequirementType(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Requirement", "FunctionalRequirement", "InterfaceRequirement", "PerformanceRequirement", "PhysicalRequirement", "DesignConstraint"]


RequirementType_reflection = _expr25

def _expr26() -> TypeInfo:
    return union_type("Siren.RDRiskType", [], RDRiskType, lambda: [[], [], []])


class RDRiskType(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Low", "Medium", "High"]


RDRiskType_reflection = _expr26

def _expr27() -> TypeInfo:
    return union_type("Siren.RDVerifyMethod", [], RDVerifyMethod, lambda: [[], [], [], []])


class RDVerifyMethod(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Analysis", "Inspection", "Test", "Demonstration"]


RDVerifyMethod_reflection = _expr27

def _expr28() -> TypeInfo:
    return union_type("Siren.RDRelationship", [], RDRelationship, lambda: [[], [], [], [], [], [], []])


class RDRelationship(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Contains", "Copies", "Derives", "Satisfies", "Verifies", "Refines", "Traces"]


RDRelationship_reflection = _expr28

def _expr29() -> TypeInfo:
    return union_type("Siren.GitCommitType", [], GitCommitType, lambda: [[], [], []])


class GitCommitType(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["NORMAL", "REVERSE", "HIGHLIGHT"]


GitCommitType_reflection = _expr29

def _expr30() -> TypeInfo:
    return union_type("Siren.MindmapShape", [], MindmapShape, lambda: [[], [], [], [], [], []])


class MindmapShape(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Square", "RoundedSquare", "Circle", "Bang", "Cloud", "Hexagon"]


MindmapShape_reflection = _expr30

def _expr31() -> TypeInfo:
    return union_type("Siren.BlockBlockType", [], BlockBlockType, lambda: [[], [], [], [], [], [], [], [], [], [], [], [], [], []])


class BlockBlockType(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Square", "RoundedEdge", "Stadium", "Subroutine", "Cylindrical", "Circle", "Asymmetric", "Rhombus", "Hexagon", "Parallelogram", "ParallelogramAlt", "Trapezoid", "TrapezoidAlt", "DoubleCircle"]


BlockBlockType_reflection = _expr31

def _expr32() -> TypeInfo:
    return union_type("Siren.BlockArrowDirection", [], BlockArrowDirection, lambda: [[], [], [], [], [], [], [("Item", string_type)]])


class BlockArrowDirection(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Right", "Left", "Up", "Down", "X", "Y", "Custom"]


BlockArrowDirection_reflection = _expr32

def _expr33() -> TypeInfo:
    return union_type("Siren.FlowchartElement", [], FlowchartElement, lambda: [[("Item", string_type)], [("opener", string_type), ("closer", string_type), ("Item3", list_type(FlowchartElement_reflection()))]])


class FlowchartElement(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["FlowchartElement", "FlowchartSubgraph"]

    def ToYamlAst(self, __unit: None=None) -> FSharpList[Yaml_AST]:
        this: FlowchartElement = self
        return YamlHelpers_writeYamlASTBasicWrapper(this.fields[0], this.fields[1], this.fields[2]) if (this.tag == 1) else singleton_1(Yaml_line(this.fields[0]))


FlowchartElement_reflection = _expr33

def _expr36() -> TypeInfo:
    return union_type("Siren.SequenceElement", [], SequenceElement, lambda: [[("Item", string_type)], [("opener", string_type), ("closer", string_type), ("Item3", list_type(SequenceElement_reflection()))], [("Item", list_type(SequenceElement_reflection()))]])


class SequenceElement(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["SequenceElement", "SequenceWrapper", "SequenceWrapperList"]

    def ToYamlAst(self, __unit: None=None) -> FSharpList[Yaml_AST]:
        this: SequenceElement = self
        if this.tag == 1:
            return YamlHelpers_writeYamlASTBasicWrapper(this.fields[0], this.fields[1], this.fields[2])

        elif this.tag == 2:
            def _arrow35(__unit: None=None) -> IEnumerable_1[Yaml_AST]:
                def _arrow34(child: SequenceElement) -> IEnumerable_1[Yaml_AST]:
                    return child.ToYamlAst()

                return collect(_arrow34, this.fields[0])

            return to_list(delay(_arrow35))

        else: 
            return singleton_1(Yaml_line(this.fields[0]))



SequenceElement_reflection = _expr36

def _expr37() -> TypeInfo:
    return union_type("Siren.ClassDiagramElement", [], ClassDiagramElement, lambda: [[("Item", string_type)], [("opener", string_type), ("closer", string_type), ("Item3", list_type(ClassDiagramElement_reflection()))], []])


class ClassDiagramElement(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["ClassDiagramElement", "ClassDiagramWrapper", "ClassDiagramNone"]

    def ToYamlAst(self, __unit: None=None) -> FSharpList[Yaml_AST]:
        this: ClassDiagramElement = self
        if this.tag == 1:
            return YamlHelpers_writeYamlASTBasicWrapper(this.fields[0], this.fields[1], this.fields[2])

        elif this.tag == 2:
            return empty_1()

        else: 
            return singleton_1(Yaml_line(this.fields[0]))



ClassDiagramElement_reflection = _expr37

def _expr38() -> TypeInfo:
    return union_type("Siren.StateDiagramElement", [], StateDiagramElement, lambda: [[("Item", string_type)], [("opener", string_type), ("closer", string_type), ("Item3", list_type(StateDiagramElement_reflection()))]])


class StateDiagramElement(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["StateDiagramElement", "StateDiagramWrapper"]

    def ToYamlAst(self, __unit: None=None) -> FSharpList[Yaml_AST]:
        this: StateDiagramElement = self
        return YamlHelpers_writeYamlASTBasicWrapper(this.fields[0], this.fields[1], this.fields[2]) if (this.tag == 1) else singleton_1(Yaml_line(this.fields[0]))


StateDiagramElement_reflection = _expr38

def _expr39() -> TypeInfo:
    return union_type("Siren.ERDiagramElement", [], ERDiagramElement, lambda: [[("Item", string_type)], [("opener", string_type), ("closer", string_type), ("Item3", list_type(ERDiagramElement_reflection()))]])


class ERDiagramElement(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["ERDiagramElement", "ERDiagramWrapper"]

    def ToYamlAst(self, __unit: None=None) -> FSharpList[Yaml_AST]:
        this: ERDiagramElement = self
        return YamlHelpers_writeYamlASTBasicWrapper(this.fields[0], this.fields[1], this.fields[2]) if (this.tag == 1) else singleton_1(Yaml_line(this.fields[0]))


ERDiagramElement_reflection = _expr39

def _expr40() -> TypeInfo:
    return union_type("Siren.JourneyElement", [], JourneyElement, lambda: [[("Item", string_type)]])


class JourneyElement(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["JourneyElement"]

    def ToYamlAst(self, __unit: None=None) -> FSharpList[Yaml_AST]:
        this: JourneyElement = self
        return singleton_1(Yaml_line(this.fields[0]))


JourneyElement_reflection = _expr40

def _expr41() -> TypeInfo:
    return union_type("Siren.GanttElement", [], GanttElement, lambda: [[("Item", string_type)]])


class GanttElement(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["GanttElement"]

    def ToYamlAst(self, __unit: None=None) -> FSharpList[Yaml_AST]:
        this: GanttElement = self
        return singleton_1(Yaml_line(this.fields[0]))


GanttElement_reflection = _expr41

def _expr42() -> TypeInfo:
    return union_type("Siren.PieChartElement", [], PieChartElement, lambda: [[("Item", string_type)]])


class PieChartElement(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["PieChartElement"]

    def ToYamlAst(self, __unit: None=None) -> FSharpList[Yaml_AST]:
        this: PieChartElement = self
        return singleton_1(Yaml_line(this.fields[0]))


PieChartElement_reflection = _expr42

def _expr43() -> TypeInfo:
    return union_type("Siren.QuadrantElement", [], QuadrantElement, lambda: [[("Item", string_type)]])


class QuadrantElement(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["QuadrantElement"]

    def ToYamlAst(self, __unit: None=None) -> FSharpList[Yaml_AST]:
        this: QuadrantElement = self
        return singleton_1(Yaml_line(this.fields[0]))


QuadrantElement_reflection = _expr43

def _expr44() -> TypeInfo:
    return union_type("Siren.RequirementDiagramElement", [], RequirementDiagramElement, lambda: [[("Item", string_type)], [("opener", string_type), ("closer", string_type), ("Item3", list_type(RequirementDiagramElement_reflection()))]])


class RequirementDiagramElement(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["RequirementDiagramElement", "RequirementDiagramWrapper"]

    def ToYamlAst(self, __unit: None=None) -> FSharpList[Yaml_AST]:
        this: RequirementDiagramElement = self
        return YamlHelpers_writeYamlASTBasicWrapper(this.fields[0], this.fields[1], this.fields[2]) if (this.tag == 1) else singleton_1(Yaml_line(this.fields[0]))


RequirementDiagramElement_reflection = _expr44

def _expr45() -> TypeInfo:
    return union_type("Siren.GitGraphElement", [], GitGraphElement, lambda: [[("Item", string_type)], [("opener", string_type), ("closer", string_type), ("Item3", list_type(GitGraphElement_reflection()))]])


class GitGraphElement(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["GitGraphElement", "GitGraphWrapper"]

    def ToYamlAst(self, __unit: None=None) -> FSharpList[Yaml_AST]:
        this: GitGraphElement = self
        return YamlHelpers_writeYamlASTBasicWrapper(this.fields[0], this.fields[1], this.fields[2]) if (this.tag == 1) else singleton_1(Yaml_line(this.fields[0]))


GitGraphElement_reflection = _expr45

def _expr46() -> TypeInfo:
    return union_type("Siren.MindmapElement", [], MindmapElement, lambda: [[("Item", string_type)], [("opener", string_type), ("closer", string_type), ("Item3", list_type(MindmapElement_reflection()))]])


class MindmapElement(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["MindmapElement", "MindmapWrapper"]

    def ToYamlAst(self, __unit: None=None) -> FSharpList[Yaml_AST]:
        this: MindmapElement = self
        return YamlHelpers_writeYamlASTBasicWrapper(this.fields[0], this.fields[1], this.fields[2]) if (this.tag == 1) else singleton_1(Yaml_line(this.fields[0]))


MindmapElement_reflection = _expr46

def _expr47() -> TypeInfo:
    return union_type("Siren.TimelineElement", [], TimelineElement, lambda: [[("Item", string_type)], [("opener", string_type), ("closer", string_type), ("Item3", list_type(TimelineElement_reflection()))]])


class TimelineElement(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["TimelineElement", "TimelineWrapper"]

    def ToYamlAst(self, __unit: None=None) -> FSharpList[Yaml_AST]:
        this: TimelineElement = self
        return YamlHelpers_writeYamlASTBasicWrapper(this.fields[0], this.fields[1], this.fields[2]) if (this.tag == 1) else singleton_1(Yaml_line(this.fields[0]))


TimelineElement_reflection = _expr47

def _expr49() -> TypeInfo:
    return union_type("Siren.BlockElement", [], BlockElement, lambda: [[("Item", string_type)], [("opener", string_type), ("closer", string_type), ("Item3", list_type(BlockElement_reflection()))], [("Item", list_type(BlockElement_reflection()))]])


class BlockElement(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["BlockElement", "BlockWrapper", "BlockLine"]

    def ToYamlAst(self, __unit: None=None) -> FSharpList[Yaml_AST]:
        this: BlockElement = self
        if this.tag == 1:
            return YamlHelpers_writeYamlASTBasicWrapper(this.fields[0], this.fields[1], this.fields[2])

        elif this.tag == 2:
            def _arrow48(__unit: None=None) -> str:
                def folder(acc: str, child: BlockElement) -> str:
                    if child.tag == 0:
                        return (acc + " ") + child.fields[0]

                    else: 
                        return acc


                _arg: str = fold(folder, "", this.fields[0])
                return _arg.strip()

            return singleton_1(Yaml_line(_arrow48()))

        else: 
            return singleton_1(Yaml_line(this.fields[0]))



BlockElement_reflection = _expr49

def _expr52() -> TypeInfo:
    return union_type("Siren.SankeyElement", [], SankeyElement, lambda: [[("Item", string_type)], [("Item", list_type(SankeyElement_reflection()))]])


class SankeyElement(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["SankeyElement", "SankeyElementList"]

    def ToYamlAst(self, __unit: None=None) -> FSharpList[Yaml_AST]:
        this: SankeyElement = self
        def _arrow51(__unit: None=None) -> IEnumerable_1[Yaml_AST]:
            def _arrow50(ele: SankeyElement) -> IEnumerable_1[Yaml_AST]:
                return ele.ToYamlAst()

            return collect(_arrow50, this.fields[0])

        return to_list(delay(_arrow51)) if (this.tag == 1) else singleton_1(Yaml_line(this.fields[0]))


SankeyElement_reflection = _expr52

def _expr53() -> TypeInfo:
    return union_type("Siren.XYChartElement", [], XYChartElement, lambda: [[("Item", string_type)]])


class XYChartElement(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["XYChartElement"]

    def ToYamlAst(self, __unit: None=None) -> FSharpList[Yaml_AST]:
        this: XYChartElement = self
        return singleton_1(Yaml_line(this.fields[0]))


XYChartElement_reflection = _expr53

def _expr61() -> TypeInfo:
    return union_type("Siren.SirenGraph", [], SirenGraph, lambda: [[("Item1", Direction_reflection()), ("Item2", list_type(FlowchartElement_reflection()))], [("Item", list_type(SequenceElement_reflection()))], [("Item", list_type(ClassDiagramElement_reflection()))], [("Item", list_type(StateDiagramElement_reflection()))], [("Item", list_type(StateDiagramElement_reflection()))], [("Item", list_type(ERDiagramElement_reflection()))], [("Item", list_type(JourneyElement_reflection()))], [("Item", list_type(GanttElement_reflection()))], [("showData", bool_type), ("title", option_type(string_type)), ("Item3", list_type(PieChartElement_reflection()))], [("Item", list_type(QuadrantElement_reflection()))], [("Item", list_type(RequirementDiagramElement_reflection()))], [("Item", list_type(GitGraphElement_reflection()))], [("Item", list_type(MindmapElement_reflection()))], [("Item", list_type(TimelineElement_reflection()))], [("Item", list_type(SankeyElement_reflection()))], [("isHorizontal", bool_type), ("Item2", list_type(XYChartElement_reflection()))], [("Item", list_type(BlockElement_reflection()))]])


class SirenGraph(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Flowchart", "Sequence", "Class", "State", "StateV2", "ERDiagram", "Journey", "Gantt", "PieChart", "Quadrant", "RequirementDiagram", "GitGraph", "Mindmap", "Timeline", "Sankey", "XYChart", "Block"]

    def ToConfigName(self, __unit: None=None) -> str:
        this: SirenGraph = self
        if this.tag == 2:
            return "class"

        elif this.tag == 1:
            return "sequence"

        elif (this.tag == 3) or (this.tag == 4):
            return "state"

        elif this.tag == 5:
            return "erDiagram"

        elif this.tag == 6:
            return "journey"

        elif this.tag == 7:
            return "gantt"

        elif this.tag == 8:
            return "pie"

        elif this.tag == 9:
            return "quadrant"

        elif this.tag == 10:
            return "requirement"

        elif this.tag == 11:
            return "gitGraph"

        elif this.tag == 12:
            return "mindmap"

        elif this.tag == 13:
            return "timeline"

        elif this.tag == 14:
            return "sankey"

        elif this.tag == 15:
            return "xyChart"

        elif this.tag == 16:
            return "block"

        else: 
            return "flowchart"


    def ToYamlAst(self, __unit: None=None) -> Yaml_AST:
        this: SirenGraph = self
        if this.tag == 1:
            return YamlHelpers_writeYamlDiagramRoot("sequenceDiagram", this.fields[0])

        elif this.tag == 2:
            return YamlHelpers_writeYamlDiagramRoot("classDiagram", this.fields[0])

        elif this.tag == 4:
            return YamlHelpers_writeYamlDiagramRoot("stateDiagram-v2", this.fields[0])

        elif this.tag == 3:
            return YamlHelpers_writeYamlDiagramRoot("stateDiagram", this.fields[0])

        elif this.tag == 5:
            return YamlHelpers_writeYamlDiagramRoot("erDiagram", this.fields[0])

        elif this.tag == 6:
            return YamlHelpers_writeYamlDiagramRoot("journey", this.fields[0])

        elif this.tag == 7:
            return YamlHelpers_writeYamlDiagramRoot("gantt", this.fields[0])

        elif this.tag == 8:
            title: str | None = this.fields[1]
            def _arrow57(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow56(__unit: None=None) -> IEnumerable_1[str]:
                    def _arrow55(__unit: None=None) -> IEnumerable_1[str]:
                        def _arrow54(__unit: None=None) -> str:
                            arg: str = value_2(title)
                            return to_text(printf("title %s"))(arg)

                        return singleton(_arrow54()) if (title is not None) else empty()

                    return append(singleton("showData"), delay(_arrow55)) if this.fields[0] else empty()

                return append(singleton("pie"), delay(_arrow56))

            return YamlHelpers_writeYamlDiagramRoot(join(" ", to_list(delay(_arrow57))), this.fields[2])

        elif this.tag == 9:
            return YamlHelpers_writeYamlDiagramRoot("quadrantChart", this.fields[0])

        elif this.tag == 10:
            return YamlHelpers_writeYamlDiagramRoot("requirementDiagram", this.fields[0])

        elif this.tag == 11:
            return YamlHelpers_writeYamlDiagramRoot("gitGraph", this.fields[0])

        elif this.tag == 12:
            return YamlHelpers_writeYamlDiagramRoot("mindmap", this.fields[0])

        elif this.tag == 13:
            return YamlHelpers_writeYamlDiagramRoot("timeline", this.fields[0])

        elif this.tag == 14:
            def _arrow60(__unit: None=None) -> IEnumerable_1[Yaml_AST]:
                def _arrow59(__unit: None=None) -> IEnumerable_1[Yaml_AST]:
                    def _arrow58(child: SankeyElement) -> IEnumerable_1[Yaml_AST]:
                        return child.ToYamlAst()

                    return collect(_arrow58, this.fields[0])

                return append(singleton(Yaml_line("sankey-beta")), delay(_arrow59))

            return Yaml_root(to_list(delay(_arrow60)))

        elif this.tag == 15:
            return YamlHelpers_writeYamlDiagramRoot("xychart-beta" + (" horizontal" if this.fields[0] else ""), this.fields[1])

        elif this.tag == 16:
            return YamlHelpers_writeYamlDiagramRoot("block-beta", this.fields[0])

        else: 
            return YamlHelpers_writeYamlDiagramRoot("flowchart " + to_string(this.fields[0]), this.fields[1])



SirenGraph_reflection = _expr61

def _expr62() -> TypeInfo:
    return union_type("Siren.ConfigVariable", [], ConfigVariable, lambda: [[("Item1", string_type), ("Item2", string_type)]])


class ConfigVariable(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["ConfigVariable"]


ConfigVariable_reflection = _expr62

def _expr63() -> TypeInfo:
    return union_type("Siren.ThemeVariable", [], ThemeVariable, lambda: [[("Item1", string_type), ("Item2", string_type)]])


class ThemeVariable(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["ThemeVariable"]


ThemeVariable_reflection = _expr63

def _expr78() -> TypeInfo:
    return class_type("Siren.SirenConfig", None, SirenConfig)


class SirenConfig:
    def __init__(self, graph: SirenGraph, title: str | None=None, theme: str | None=None, graph_config: Array[ConfigVariable] | None=None, theme_variable: Array[ThemeVariable] | None=None) -> None:
        self._Graph: SirenGraph = graph
        self._Title: str | None = title
        self._Theme: str | None = theme
        self._GraphConfig: Array[ConfigVariable] | None = graph_config
        self._ThemeVariables: Array[ThemeVariable] | None = theme_variable

    @property
    def Graph(self, __unit: None=None) -> SirenGraph:
        __: SirenConfig = self
        return __._Graph

    @property
    def Title(self, __unit: None=None) -> str | None:
        __: SirenConfig = self
        return __._Title

    @Title.setter
    def Title(self, v: str | None=None) -> None:
        __: SirenConfig = self
        __._Title = v

    @property
    def Theme(self, __unit: None=None) -> str | None:
        __: SirenConfig = self
        return __._Theme

    @Theme.setter
    def Theme(self, v: str | None=None) -> None:
        __: SirenConfig = self
        __._Theme = v

    @property
    def GraphConfig(self, __unit: None=None) -> Array[ConfigVariable] | None:
        __: SirenConfig = self
        return __._GraphConfig

    @GraphConfig.setter
    def GraphConfig(self, v: Array[ConfigVariable] | None=None) -> None:
        __: SirenConfig = self
        __._GraphConfig = v

    @property
    def ThemeVariables(self, __unit: None=None) -> Array[ThemeVariable] | None:
        __: SirenConfig = self
        return __._ThemeVariables

    @ThemeVariables.setter
    def ThemeVariables(self, v: Array[ThemeVariable] | None=None) -> None:
        __: SirenConfig = self
        __._ThemeVariables = v

    def AddGraphConfig(self, var: ConfigVariable) -> None:
        this: SirenConfig = self
        match_value: Array[ConfigVariable] | None = this.GraphConfig
        if match_value is None:
            config_1: Array[ConfigVariable] = []
            (config_1.append(var))
            this.GraphConfig = config_1

        else: 
            config: Array[ConfigVariable] = match_value
            (config.append(var))


    def AddThemeVariable(self, var: ThemeVariable) -> None:
        this: SirenConfig = self
        match_value: Array[ThemeVariable] | None = this.ThemeVariables
        if match_value is None:
            theme_1: Array[ThemeVariable] = []
            (theme_1.append(var))
            this.ThemeVariables = theme_1

        else: 
            theme: Array[ThemeVariable] = match_value
            (theme.append(var))


    def ToYamlAst(self, __unit: None=None) -> Yaml_AST:
        this: SirenConfig = self
        has_inner_config: bool = True if (True if (this.GraphConfig is not None) else (this.ThemeVariables is not None)) else (this.Theme is not None)
        def _arrow77(__unit: None=None) -> IEnumerable_1[Yaml_AST]:
            def _arrow76(__unit: None=None) -> IEnumerable_1[Yaml_AST]:
                def _arrow75(__unit: None=None) -> IEnumerable_1[Yaml_AST]:
                    def _arrow73(__unit: None=None) -> IEnumerable_1[Yaml_AST]:
                        def _arrow72(__unit: None=None) -> IEnumerable_1[Yaml_AST]:
                            def _arrow67(__unit: None=None) -> IEnumerable_1[Yaml_AST]:
                                match_value: Array[ConfigVariable] | None = this.GraphConfig
                                if match_value is None:
                                    return empty()

                                else: 
                                    config: Array[ConfigVariable] = match_value
                                    def _arrow66(__unit: None=None) -> IEnumerable_1[Yaml_AST]:
                                        def _arrow65(__unit: None=None) -> IEnumerable_1[Yaml_AST]:
                                            def _arrow64(match_value_1: ConfigVariable) -> IEnumerable_1[Yaml_AST]:
                                                return singleton(Yaml_line(((("" + match_value_1.fields[0]) + ": ") + match_value_1.fields[1]) + ""))

                                            return collect(_arrow64, config)

                                        return singleton(Yaml_level(to_list(delay(_arrow65))))

                                    return append(singleton(Yaml_line(this.Graph.ToConfigName() + ":")), delay(_arrow66))


                            def _arrow71(__unit: None=None) -> IEnumerable_1[Yaml_AST]:
                                match_value_2: Array[ThemeVariable] | None = this.ThemeVariables
                                if match_value_2 is None:
                                    return empty()

                                else: 
                                    theme: Array[ThemeVariable] = match_value_2
                                    def _arrow70(__unit: None=None) -> IEnumerable_1[Yaml_AST]:
                                        def _arrow69(__unit: None=None) -> IEnumerable_1[Yaml_AST]:
                                            def _arrow68(match_value_3: ThemeVariable) -> IEnumerable_1[Yaml_AST]:
                                                return singleton(Yaml_line(((("" + match_value_3.fields[0]) + ": ") + match_value_3.fields[1]) + ""))

                                            return collect(_arrow68, theme)

                                        return singleton(Yaml_level(to_list(delay(_arrow69))))

                                    return append(singleton(Yaml_line("themeVariables:")), delay(_arrow70))


                            return append(_arrow67(), delay(_arrow71))

                        return append(singleton(Yaml_line(("theme: " + value_2(this.Theme)) + "")) if (this.Theme is not None) else empty(), delay(_arrow72))

                    def _arrow74(__unit: None=None) -> IEnumerable_1[Yaml_AST]:
                        return singleton(Yaml_line("---"))

                    return append(singleton(Yaml_root(of_array([Yaml_line("config:"), Yaml_level(to_list(delay(_arrow73)))]))) if has_inner_config else empty(), delay(_arrow74))

                return append(singleton(Yaml_line(("title: " + value_2(this.Title)) + "")) if (this.Title is not None) else empty(), delay(_arrow75))

            return append(singleton(Yaml_line("---")), delay(_arrow76)) if (True if (this.Title is not None) else has_inner_config) else empty()

        return Yaml_root(to_list(delay(_arrow77)))

    def __str__(self, __unit: None=None) -> str:
        this: SirenConfig = self
        def mapping_2(tupled_arg: tuple[str, str]) -> str:
            return to_text(printf("%s: %s"))(tupled_arg[0])(tupled_arg[1])

        arg_2: str = join(",\n", map(mapping_2, of_array([("Title", to_string(this.Title)), ("Theme", to_string(this.Theme)), ("GraphConfig", to_string(map_1(seq_to_string, this.GraphConfig))), ("ThemeVariables", to_string(map_1(seq_to_string, this.ThemeVariables)))])))
        return to_text(printf("{%s}"))(arg_2)


SirenConfig_reflection = _expr78

def SirenConfig__ctor_4F11949C(graph: SirenGraph, title: str | None=None, theme: str | None=None, graph_config: Array[ConfigVariable] | None=None, theme_variable: Array[ThemeVariable] | None=None) -> SirenConfig:
    return SirenConfig(graph, title, theme, graph_config, theme_variable)


def _expr79() -> TypeInfo:
    return record_type("Siren.SirenElement", [], SirenElement, lambda: [("Graph", SirenGraph_reflection()), ("Config", SirenConfig_reflection())])


@dataclass(eq = False, repr = False, slots = True)
class SirenElement(Record):
    Graph: SirenGraph
    Config: SirenConfig
    @staticmethod
    def init(graph: SirenGraph) -> SirenElement:
        return SirenElement(graph, SirenConfig(graph))

    def with_title(self, title: str) -> SirenElement:
        this: SirenElement = self
        this.Config.Title = title
        return this

    def with_theme(self, theme: str) -> SirenElement:
        this: SirenElement = self
        this.Config.Theme = theme
        return this

    def with_graph_config(self, config_func: Callable[[Array[ConfigVariable]], None]) -> SirenElement:
        this: SirenElement = self
        config: Array[ConfigVariable] = default_arg(this.Config.GraphConfig, [])
        config_func(config)
        this.Config.GraphConfig = config
        return this

    def with_theme_variables(self, theme_variables_func: Callable[[Array[ThemeVariable]], None]) -> SirenElement:
        this: SirenElement = self
        theme_variables: Array[ThemeVariable] = default_arg(this.Config.ThemeVariables, [])
        theme_variables_func(theme_variables)
        this.Config.ThemeVariables = theme_variables
        return this

    def add_theme_variable(self, var: ThemeVariable) -> SirenElement:
        this: SirenElement = self
        this.Config.AddThemeVariable(var)
        return this

    def add_graph_config_variable(self, var: ConfigVariable) -> SirenElement:
        this: SirenElement = self
        this.Config.AddGraphConfig(var)
        return this

    def write(self, __unit: None=None) -> str:
        this: SirenElement = self
        return Yaml_write(Yaml_root(of_array([this.Config.ToYamlAst(), this.Graph.ToYamlAst()])))


SirenElement_reflection = _expr79

__all__ = ["YamlHelpers_writeYamlASTBasicWrapper", "YamlHelpers_writeYamlDiagramRoot", "NotePosition_reflection", "Direction_reflection", "FlowchartNodeTypes_reflection", "FlowchartLinkTypes_reflection", "SequenceMessageTypes_reflection", "ClassMemberVisibility_reflection", "ClassMemberClassifier_reflection", "ClassRelationshipDirection_reflection", "ClassRelationshipType_reflection", "ClassCardinality_reflection", "ERCardinalityType_reflection", "ERKeyType_reflection", "ERAttribute_reflection", "GanttTags_reflection", "GanttUnit_reflection", "RequirementType_reflection", "RDRiskType_reflection", "RDVerifyMethod_reflection", "RDRelationship_reflection", "GitCommitType_reflection", "MindmapShape_reflection", "BlockBlockType_reflection", "BlockArrowDirection_reflection", "FlowchartElement_reflection", "SequenceElement_reflection", "ClassDiagramElement_reflection", "StateDiagramElement_reflection", "ERDiagramElement_reflection", "JourneyElement_reflection", "GanttElement_reflection", "PieChartElement_reflection", "QuadrantElement_reflection", "RequirementDiagramElement_reflection", "GitGraphElement_reflection", "MindmapElement_reflection", "TimelineElement_reflection", "BlockElement_reflection", "SankeyElement_reflection", "XYChartElement_reflection", "SirenGraph_reflection", "ConfigVariable_reflection", "ThemeVariable_reflection", "SirenConfig_reflection", "SirenElement_reflection"]

