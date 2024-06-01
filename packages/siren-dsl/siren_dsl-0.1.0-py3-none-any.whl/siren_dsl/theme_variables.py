from __future__ import annotations
from typing import Any
from .fable-library.reflection import (TypeInfo, class_type)
from .fable-library.string_ import join
from .fable-library.util import int32_to_string
from .siren_types import ThemeVariable

def _expr80() -> TypeInfo:
    return class_type("Siren.themeVariable", None, themeVariable)


class theme_variable:
    @staticmethod
    def custom(key: str, value: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = (key, value)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])


themeVariable_reflection = _expr80

def _expr81() -> TypeInfo:
    return class_type("Siren.quadrantTheme", None, quadrantTheme)


class quadrant_theme:
    @staticmethod
    def custom(key: str, value: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = (key, value)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def quadrant1fill(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("quadrant1Fill", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def quadrant2fill(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("quadrant2Fill", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def quadrant3fill(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("quadrant3Fill", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def quadrant4fill(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("quadrant4Fill", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def quadrant1text_fill(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("quadrant1TextFill", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def quadrant2text_fill(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("quadrant2TextFill", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def quadrant3text_fill(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("quadrant3TextFill", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def quadrant4text_fill(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("quadrant4TextFill", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def quadrant_point_fill(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("quadrantPointFill", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def quadrant_point_text_fill(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("quadrantPointTextFill", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def quadrant_xaxis_text_fill(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("quadrantXAxisTextFill", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def quadrant_yaxis_text_fill(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("quadrantYAxisTextFill", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def quadrant_internal_border_stroke_fill(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("quadrantInternalBorderStrokeFill", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def quadrant_external_border_stroke_fill(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("quadrantExternalBorderStrokeFill", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def quadrant_title_fill(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("quadrantTitleFill", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])


quadrantTheme_reflection = _expr81

def _expr82() -> TypeInfo:
    return class_type("Siren.gitTheme", None, gitTheme)


class git_theme:
    @staticmethod
    def custom(key: str, value: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = (key, value)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def git0(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("git0", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def git1(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("git1", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def git2(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("git2", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def git3(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("git3", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def git4(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("git4", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def git5(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("git5", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def git6(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("git6", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def git7(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("git7", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def git_branch_label0(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("gitBranchLabel0", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def git_branch_label1(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("gitBranchLabel1", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def git_branch_label2(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("gitBranchLabel2", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def git_branch_label3(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("gitBranchLabel3", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def git_branch_label4(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("gitBranchLabel4", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def git_branch_label5(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("gitBranchLabel5", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def git_branch_label6(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("gitBranchLabel6", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def git_branch_label7(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("gitBranchLabel7", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def git_branch_label8(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("gitBranchLabel8", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def git_branch_label9(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("gitBranchLabel9", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def commit_label_color(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("commitLabelColor", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def commit_label_background(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("commitLabelBackground", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def commit_label_font_size(length_unit: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("commitLabelFontSize", length_unit)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def commit_label_font_size_px(length_unit: int) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("commitLabelFontSize", int32_to_string(length_unit) + "px")
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def tag_label_font_size(length_unit: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("tagLabelFontSize", length_unit)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def tag_label_font_size_px(length_unit: int) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("tagLabelFontSize", int32_to_string(length_unit) + "px")
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def tag_label_color(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("tagLabelColor", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def tag_label_background(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("tagLabelBackground", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def tag_label_border(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("tagLabelBorder", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def git_inv0(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("gitInv0", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def git_inv1(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("gitInv1", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def git_inv2(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("gitInv2", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def git_inv3(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("gitInv3", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def git_inv4(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("gitInv4", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def git_inv5(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("gitInv5", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def git_inv6(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("gitInv6", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def git_inv7(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("gitInv7", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])


gitTheme_reflection = _expr82

def _expr83() -> TypeInfo:
    return class_type("Siren.timelineTheme", None, timelineTheme)


class timeline_theme:
    @staticmethod
    def custom(key: str, value: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = (key, value)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def c_scale0(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("cScale0", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def c_scale1(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("cScale1", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def c_scale2(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("cScale2", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def c_scale3(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("cScale3", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def c_scale4(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("cScale4", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def c_scale5(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("cScale5", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def c_scale6(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("cScale6", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def c_scale7(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("cScale7", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def c_scale8(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("cScale8", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def c_scale9(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("cScale9", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def c_scale10(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("cScale10", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def c_scale11(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("cScale11", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def c_scale_label0(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("cScaleLabel0", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def c_scale_label1(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("cScaleLabel1", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def c_scale_label2(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("cScaleLabel2", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def c_scale_label3(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("cScaleLabel3", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def c_scale_label4(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("cScaleLabel4", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def c_scale_label5(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("cScaleLabel5", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def c_scale_label6(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("cScaleLabel6", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def c_scale_label7(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("cScaleLabel7", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def c_scale_label8(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("cScaleLabel8", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def c_scale_label9(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("cScaleLabel9", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def c_scale_label10(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("cScaleLabel10", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def c_scale_label11(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("cScaleLabel11", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])


timelineTheme_reflection = _expr83

def _expr84() -> TypeInfo:
    return class_type("Siren.xyChartTheme", None, xyChartTheme)


class xy_chart_theme:
    @staticmethod
    def custom(key: str, value: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = (key, value)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def background_color(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("backgroundColor", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def title_color(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("titleColor", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def x_axis_label_color(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("xAxisLabelColor", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def x_axis_title_color(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("xAxisTitleColor", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def x_axis_tick_color(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("xAxisTickColor", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def x_axis_line_color(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("xAxisLineColor", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def y_axis_label_color(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("yAxisLabelColor", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def y_axis_title_color(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("yAxisTitleColor", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def y_axis_tick_color(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("yAxisTickColor", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def y_axis_line_color(color: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("yAxisLineColor", color)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def plot_color_palette(colors: Any | None=None) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("plotColorPalette", join(",", colors))
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])


xyChartTheme_reflection = _expr84

def _expr85() -> TypeInfo:
    return class_type("Siren.pieTheme", None, pieTheme)


class pie_theme:
    @staticmethod
    def custom(key: str, value: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = (key, value)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])

    @staticmethod
    def pie_outer_stroke_width(length_unit: str) -> ThemeVariable:
        tupled_arg: tuple[str, str] = ("pieOuterStrokeWidth", length_unit)
        return ThemeVariable(0, tupled_arg[0], tupled_arg[1])


pieTheme_reflection = _expr85

__all__ = ["themeVariable_reflection", "quadrantTheme_reflection", "gitTheme_reflection", "timelineTheme_reflection", "xyChartTheme_reflection", "pieTheme_reflection"]

