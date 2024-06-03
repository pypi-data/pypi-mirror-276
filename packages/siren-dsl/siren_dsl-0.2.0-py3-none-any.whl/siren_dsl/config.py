from __future__ import annotations
from typing import Any
from .fable-library.list import (map, FSharpList, choose, of_array)
from .fable-library.reflection import (TypeInfo, class_type)
from .fable-library.string_ import (to_text, printf, join)
from .fable-library.types import to_string
from .fable-library.util import int32_to_string
from .siren_types import ConfigVariable
from .util import Bool_toString

def _expr86() -> TypeInfo:
    return class_type("Siren.graphConfig", None, graphConfig)


class graph_config:
    @staticmethod
    def custom(key: str, value: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = (key, value)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])


graphConfig_reflection = _expr86

def _expr87() -> TypeInfo:
    return class_type("Siren.flowchartConfig", None, flowchartConfig)


class flowchart_config:
    @staticmethod
    def custom(key: str, value: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = (key, value)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def default_renderer(renderer: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("defaultRenderer", renderer)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def default_renderer_elk() -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("defaultRenderer", "elk")
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def default_renderer_dagre_d3() -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("defaultRenderer", "dagre-d3")
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def default_renderer_dagre_wrapper() -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("defaultRenderer", "dagre-wrapper")
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def title_top_margin(px: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("titleTopMargin", int32_to_string(px))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def sub_graph_title_margin(top: int, bottom: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("subGraphTitleMargin", to_text(printf("{\"top\": %i, \"bottom\": %i}"))(top)(bottom))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def arrow_marker_absolute(b: bool) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("arrowMarkerAbsolute", Bool_toString(b))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def diagram_padding(px: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("diagramPadding", int32_to_string(px))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def html_labels(b: bool) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("htmlLabels", Bool_toString(b))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def node_spacing(px: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("nodeSpacing", int32_to_string(px))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def rank_spacing(px: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("rankSpacing", int32_to_string(px))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def curve(name: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("curve", name)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def curve_basis() -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("curve", "basis")
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def curve_linear() -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("curve", "linear")
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def curve_cardianal() -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("curve", "cardinal")
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def padding(px: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("padding", int32_to_string(px))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def wrapping_width(px: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("wrappingWidth", int32_to_string(px))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])


flowchartConfig_reflection = _expr87

def _expr88() -> TypeInfo:
    return class_type("Siren.sequenceConfig", None, sequenceConfig)


class sequence_config:
    @staticmethod
    def custom(key: str, value: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = (key, value)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def arrow_marker_absolute(b: bool) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("arrowMarkerAbsolute", Bool_toString(b))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def hide_unused_participants(b: bool) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("hideUnusedParticipants", Bool_toString(b))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def activation_width(px: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("activationWidth", int32_to_string(px))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def diagram_margin_x(px: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("diagramMarginX", int32_to_string(px))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def diagram_margin_y(px: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("diagramMarginX", int32_to_string(px))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def actor_margin(px: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("actorMargin", int32_to_string(px))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def width(px: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("width", int32_to_string(px))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def height(px: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("height", int32_to_string(px))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def box_margin(px: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("boxMargin", int32_to_string(px))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def box_text_margin(px: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("boxTextMargin", int32_to_string(px))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def note_margin(px: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("noteMargin", int32_to_string(px))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def message_align(name: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("messageAlign", name)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def message_align_left() -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("messageAlign", "left")
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def message_alignc_center() -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("messageAlign", "center")
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def message_align_right() -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("messageAlign", "right")
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def mirror_actors(b: bool) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("mirrorActors", Bool_toString(b))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def bottom_margin_adj(px: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("bottomMarginAdj", int32_to_string(px))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def show_sequence_numbers(b: bool) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("showSequenceNumbers", Bool_toString(b))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def actor_font_size(s: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("actorFontSize", s)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def actor_font_weight(s: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("actorFontWeight", s)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def note_font_size(s: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("noteFontSize", s)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def note_font_weight(s: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("noteFontWeight", s)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def note_align(s: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("noteAlign", s)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def note_align_left() -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("noteAlign", "left")
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def note_align_center() -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("noteAlign", "center")
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def note_align_right() -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("noteAlign", "right")
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def message_font_size(s: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("messageFontSize", s)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def message_font_weight(s: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("messageFontWeight", s)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def wrap(b: bool) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("wrap", Bool_toString(b))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def wrap_padding(px: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("wrapPadding", int32_to_string(px))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])


sequenceConfig_reflection = _expr88

def _expr119() -> TypeInfo:
    return class_type("Siren.ganttConfig", None, ganttConfig)


class gantt_config:
    @staticmethod
    def custom(key: str, value: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = (key, value)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def title_top_margin(px: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("titleTopMargin", int32_to_string(px))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def bar_height(px: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("barHeight", int32_to_string(px))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def bar_gap(px: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("barGap", int32_to_string(px))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def top_padding(px: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("topPadding", int32_to_string(px))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def left_padding(px: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("leftPadding", int32_to_string(px))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def right_padding(px: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("rightPadding", int32_to_string(px))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def grid_line_start_padding(px: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("gridLineStartPadding", int32_to_string(px))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def font_size(px: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("fontSize", int32_to_string(px))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def section_font_size(px: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("sectionFontSize", int32_to_string(px))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def number_section_styles(n: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("numberSectionStyles", int32_to_string(n))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def axis_format(format: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("axisFormat", format)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def tick_interval(format: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("tickInterval", format)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def tick_interval_millisecond(ms: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("tickInterval", to_text(printf("%imillisecond"))(ms))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def tick_interval_second(s: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("tickInterval", to_text(printf("%isecond"))(s))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def tick_interval_minute(min: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("tickInterval", to_text(printf("%iminute"))(min))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def tick_interval_hour(hour: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("tickInterval", to_text(printf("%ihour"))(hour))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def tick_interval_day(day: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("tickInterval", to_text(printf("%iday"))(day))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def tick_interval_week(week: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("tickInterval", to_text(printf("%iweek"))(week))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def tick_interval_month(month: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("tickInterval", to_text(printf("%imonth"))(month))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def top_axis(b: bool) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("topAxis", Bool_toString(b))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def display_mode(mode: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("displayMode", to_text(printf("\"%s\""))(mode))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def display_mode_default() -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("displayMode", to_text(printf("\"\"")))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def display_mode_compact() -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("displayMode", to_text(printf("\"compact\"")))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def weekday(day: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("weekday", to_text(printf("%A"))(day))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def weekday_monday() -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("weekday", to_text(printf("%A"))("monday"))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def weekday_tuesday() -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("weekday", to_text(printf("%A"))("tuesday"))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def weekday_wednesday() -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("weekday", to_text(printf("%A"))("wednesday"))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def weekday_thursday() -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("weekday", to_text(printf("%A"))("thursday"))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def weekday_friday() -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("weekday", to_text(printf("%A"))("friday"))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def weekday_saturday() -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("weekday", to_text(printf("%A"))("saturday"))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def weekday_sunday() -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("weekday", to_text(printf("%A"))("sunday"))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])


ganttConfig_reflection = _expr119

def _expr121() -> TypeInfo:
    return class_type("Siren.journeyConfig", None, journeyConfig)


class journey_config:
    @staticmethod
    def custom(key: str, value: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = (key, value)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def diagram_margin_x(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("diagramMarginX", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def diagram_margin_y(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("diagramMarginY", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def left_margin(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("leftMargin", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def width(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("width", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def height(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("height", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])


journeyConfig_reflection = _expr121

def _expr122() -> TypeInfo:
    return class_type("Siren.timelineConfig", None, timelineConfig)


class timeline_config:
    @staticmethod
    def custom(key: str, value: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = (key, value)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def disable_multicolor(value: bool) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("disableMulticolor", Bool_toString(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def padding(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("disableMulticolor", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])


timelineConfig_reflection = _expr122

def _expr123() -> TypeInfo:
    return class_type("Siren.classConfig", None, classConfig)


class class_config:
    @staticmethod
    def custom(key: str, value: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = (key, value)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def default_renderer(renderer: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("defaultRenderer", renderer)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def default_renderer_elk() -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("defaultRenderer", "elk")
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def default_renderer_dagre_d3() -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("defaultRenderer", "dagre-d3")
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def default_renderer_dagre_wrapper() -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("defaultRenderer", "dagre-wrapper")
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])


classConfig_reflection = _expr123

def _expr124() -> TypeInfo:
    return class_type("Siren.stateConfig", None, stateConfig)


class state_config:
    @staticmethod
    def custom(key: str, value: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = (key, value)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def title_top_margin(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("titleTopMargin", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])


stateConfig_reflection = _expr124

def _expr126() -> TypeInfo:
    return class_type("Siren.erConfig", None, erConfig)


class er_config:
    @staticmethod
    def custom(key: str, value: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = (key, value)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def title_top_margin(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("titleTopMargin", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def diagram_padding(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("diagramPadding", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def layout_direction(value: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("layoutDirection", value)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def layout_direction_tb() -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("layoutDirection", "TB")
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def layout_direction_bt() -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("layoutDirection", "BT")
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def layout_direction_lr() -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("layoutDirection", "LR")
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def layout_direction_rl() -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("layoutDirection", "RL")
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def min_entity_width(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("minEntityWidth", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def min_entity_height(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("minEntityHeight", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def entity_padding(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("entityPadding", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def stroke(value: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("stroke", value)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def font_size(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("fontSize", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])


erConfig_reflection = _expr126

def _expr132() -> TypeInfo:
    return class_type("Siren.quadrantChartConfig", None, quadrantChartConfig)


class quadrant_chart_config:
    @staticmethod
    def custom(key: str, value: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = (key, value)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def chart_width(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("chartWidth", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def chart_height(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("chartHeight", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def title_font_size(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("titleFontSize", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def title_padding(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("titlePadding", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def quadrant_padding(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("quadrantPadding", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def x_axis_label_padding(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("xAxisLabelPadding", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def y_axis_label_padding(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("yAxisLabelPadding", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def x_axis_label_font_size(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("xAxisLabelFontSize", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def y_axis_label_font_size(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("yAxisLabelFontSize", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def quadrant_label_font_size(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("quadrantLabelFontSize", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def quadrant_text_top_padding(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("quadrantTextTopPadding", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def point_text_padding(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("pointTextPadding", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def point_label_font_size(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("pointLabelFontSize", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def point_radius(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("pointRadius", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def y_axis_position(value: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("xAxisPosition", value)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def y_axis_position_left() -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("xAxisPosition", "left")
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def y_axis_position_right() -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("xAxisPosition", "right")
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def quadrant_internal_border_stroke_width(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("quadrantInternalBorderStrokeWidth", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def quadrant_external_border_stroke_width(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("quadrantExternalBorderStrokeWidth", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])


quadrantChartConfig_reflection = _expr132

def _expr133() -> TypeInfo:
    return class_type("Siren.pieConfig", None, pieConfig)


class pie_config:
    @staticmethod
    def custom(key: str, value: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = (key, value)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def text_position(value: float) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("textPosition", to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])


pieConfig_reflection = _expr133

def _expr136() -> TypeInfo:
    return class_type("Siren.sankeyConfig", None, sankeyConfig)


class sankey_config:
    @staticmethod
    def custom(key: str, value: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = (key, value)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def width(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("width", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def height(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("width", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def link_color(value: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("linkColor", value)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def link_color_source() -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("linkColor", "source")
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def link_color_target() -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("linkColor", "target")
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def link_color_gradient() -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("linkColor", "gradient")
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])


sankeyConfig_reflection = _expr136

def XYChartHelpers_mkAxisConfig(parameters: FSharpList[tuple[str, str]]) -> str:
    def mapping(tupled_arg: tuple[str, str], parameters: Any=parameters) -> str:
        return to_text(printf("\"%s\": %A"))(tupled_arg[0])(tupled_arg[1])

    return ("{" + join(", ", map(mapping, parameters))) + "}"


def _expr150() -> TypeInfo:
    return class_type("Siren.xyChartConfig", None, xyChartConfig)


class xy_chart_config:
    @staticmethod
    def custom(key: str, value: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = (key, value)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def width(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("width", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def height(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("height", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def title_padding(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("titlePadding", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def title_font_size(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("titleFontSize", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def show_title(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("showTitle", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def _axis(name: str, show_label: bool | None=None, label_font_size: int | None=None, label_padding: int | None=None, show_title: bool | None=None, title_font_size: int | None=None, title_padding: int | None=None, show_tick: bool | None=None, tick_length: int | None=None, tick_width: int | None=None, show_axis_line: bool | None=None, axis_line_width: int | None=None) -> tuple[str, str]:
        def chooser(x: tuple[str, str] | None=None) -> tuple[str, str] | None:
            return x

        def _arrow139(__unit: None=None) -> tuple[str, str] | None:
            value: bool | None = show_label
            return None if (value is None) else (("showLabel", Bool_toString(value)))

        def _arrow140(__unit: None=None) -> tuple[str, str] | None:
            value_2: int | None = label_font_size
            return None if (value_2 is None) else (("labelFontSize", int32_to_string(value_2)))

        def _arrow141(__unit: None=None) -> tuple[str, str] | None:
            value_3: int | None = label_padding
            return None if (value_3 is None) else (("labelPadding", int32_to_string(value_3)))

        def _arrow142(__unit: None=None) -> tuple[str, str] | None:
            value_4: bool | None = show_title
            return None if (value_4 is None) else (("showTitle", Bool_toString(value_4)))

        def _arrow143(__unit: None=None) -> tuple[str, str] | None:
            value_5: int | None = title_font_size
            return None if (value_5 is None) else (("titleFontSize", int32_to_string(value_5)))

        def _arrow144(__unit: None=None) -> tuple[str, str] | None:
            value_6: int | None = title_padding
            return None if (value_6 is None) else (("titlePadding", int32_to_string(value_6)))

        def _arrow145(__unit: None=None) -> tuple[str, str] | None:
            value_7: bool | None = show_tick
            return None if (value_7 is None) else (("showTick", Bool_toString(value_7)))

        def _arrow146(__unit: None=None) -> tuple[str, str] | None:
            value_8: int | None = tick_length
            return None if (value_8 is None) else (("tickLength", int32_to_string(value_8)))

        def _arrow147(__unit: None=None) -> tuple[str, str] | None:
            value_9: int | None = tick_width
            return None if (value_9 is None) else (("tickWidth", int32_to_string(value_9)))

        def _arrow148(__unit: None=None) -> tuple[str, str] | None:
            value_10: bool | None = show_axis_line
            return None if (value_10 is None) else (("showAxisLine", Bool_toString(value_10)))

        def _arrow149(__unit: None=None) -> tuple[str, str] | None:
            value_11: int | None = axis_line_width
            return None if (value_11 is None) else (("axisLineWidth", int32_to_string(value_11)))

        return (name, XYChartHelpers_mkAxisConfig(choose(chooser, of_array([_arrow139(), _arrow140(), _arrow141(), _arrow142(), _arrow143(), _arrow144(), _arrow145(), _arrow146(), _arrow147(), _arrow148(), _arrow149()]))))

    @staticmethod
    def x_axis(show_label: bool | None=None, label_font_size: int | None=None, label_padding: int | None=None, show_title: bool | None=None, title_font_size: int | None=None, title_padding: int | None=None, show_tick: bool | None=None, tick_length: int | None=None, tick_width: int | None=None, show_axis_line: bool | None=None, axis_line_width: int | None=None) -> ConfigVariable:
        tupled_arg: tuple[str, str] = xyChartConfig._axis("xAxis", show_label, label_font_size, label_padding, show_title, title_font_size, title_padding, show_tick, tick_length, tick_width, show_axis_line, axis_line_width)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def y_axis(show_label: bool | None=None, label_font_size: int | None=None, label_padding: int | None=None, show_title: bool | None=None, title_font_size: int | None=None, title_padding: int | None=None, show_tick: bool | None=None, tick_length: int | None=None, tick_width: int | None=None, show_axis_line: bool | None=None, axis_line_width: int | None=None) -> ConfigVariable:
        tupled_arg: tuple[str, str] = xyChartConfig._axis("yAxis", show_label, label_font_size, label_padding, show_title, title_font_size, title_padding, show_tick, tick_length, tick_width, show_axis_line, axis_line_width)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def chart_orientation(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("chartOrientation", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def chart_orientation_vertical() -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("chartOrientation", "vertical")
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def chart_orientation_horizontal() -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("chartOrientation", "horizontal")
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])


xyChartConfig_reflection = _expr150

def _expr151() -> TypeInfo:
    return class_type("Siren.mindmapConfig", None, mindmapConfig)


class mindmap_config:
    @staticmethod
    def custom(key: str, value: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = (key, value)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def padding(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("padding", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def max_node_width(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("maxNodeWidth", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])


mindmapConfig_reflection = _expr151

def _expr152() -> TypeInfo:
    return class_type("Siren.gitGraphConfig", None, gitGraphConfig)


class git_graph_config:
    @staticmethod
    def custom(key: str, value: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = (key, value)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def title_top_margin(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("titleTopMargin", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def diagram_padding(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("diagramPadding", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def main_branch_name(value: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("mainBranchName", value)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def main_branch_order(value: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("mainBranchOrder", value)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def show_commit_label(value: bool) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("showCommitLabel", Bool_toString(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def show_branches(value: bool) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("showBranches", Bool_toString(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def rotate_commit_label(value: bool) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("rotateCommitLabel", Bool_toString(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def parallel_commits(value: bool) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("parallelCommits", Bool_toString(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])


gitGraphConfig_reflection = _expr152

def _expr153() -> TypeInfo:
    return class_type("Siren.requirementConfig", None, requirementConfig)


class requirement_config:
    @staticmethod
    def custom(key: str, value: str) -> ConfigVariable:
        tupled_arg: tuple[str, str] = (key, value)
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def rect_min_width(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("rect_min_width", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def rect_min_height(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("rect_min_height", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def rect_padding(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("rect_padding", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def line_height(value: int) -> ConfigVariable:
        tupled_arg: tuple[str, str] = ("line_height", int32_to_string(value))
        return ConfigVariable(0, tupled_arg[0], tupled_arg[1])


requirementConfig_reflection = _expr153

__all__ = ["graphConfig_reflection", "flowchartConfig_reflection", "sequenceConfig_reflection", "ganttConfig_reflection", "journeyConfig_reflection", "timelineConfig_reflection", "classConfig_reflection", "stateConfig_reflection", "erConfig_reflection", "quadrantChartConfig_reflection", "pieConfig_reflection", "sankeyConfig_reflection", "XYChartHelpers_mkAxisConfig", "xyChartConfig_reflection", "mindmapConfig_reflection", "gitGraphConfig_reflection", "requirementConfig_reflection"]

