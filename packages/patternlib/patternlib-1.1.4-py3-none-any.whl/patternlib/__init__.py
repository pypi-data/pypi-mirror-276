# -*- coding: utf-8 -*-

# Pattern library constants and exports.

VERSION = "1.1.4"

# ALPHABETS
from patternlib.alphabets.l_pattern import l_pattern
from patternlib.alphabets.e_pattern import e_pattern
from patternlib.alphabets.h_pattern import h_pattern
from patternlib.alphabets.i_pattern import i_pattern
from patternlib.alphabets.t_pattern import t_pattern
from patternlib.alphabets.f_pattern import f_pattern
from patternlib.alphabets.a_pattern import a_pattern
from patternlib.alphabets.v_pattern import v_pattern
from patternlib.alphabets.x_pattern import x_pattern
from patternlib.alphabets.z_pattern import z_pattern

# SHAPES
# Number Triangles
from patternlib.shapes.triangle.right_angle_triangle_pattern import right_angle_triangle_pattern
from patternlib.shapes.triangle.same_number_as_row_right_angle_triangle import same_number_as_row_right_angle_triangle
from patternlib.shapes.triangle.custom_string_right_angle_triangle import custom_string_right_angle_triangle
from patternlib.shapes.triangle.string_triangle_pointing_right import string_triangle_pointing_right
from patternlib.shapes.triangle.right_angle_triangle_inverted_across_hplane import right_angle_triangle_inverted_across_hplane
from patternlib.shapes.triangle.right_angle_triangle_inverted_across_h_and_v_plane import right_angle_triangle_inverted_across_h_and_v_plane
from patternlib.shapes.triangle.right_angle_triangle_inverted_across_vplane import right_angle_triangle_inverted_across_vplane
from patternlib.shapes.triangle.triangle_pointing_right import triangle_pointing_right
from patternlib.shapes.triangle.triangle_pointing_right_double_center_row import triangle_pointing_right_double_center_row
from patternlib.shapes.triangle.triangle_pointing_left import triangle_pointing_left
from patternlib.shapes.triangle.triangle_pointing_left_double_center_row import triangle_pointing_left_double_center_row
from patternlib.shapes.triangle.isosceles_triangle_pointing_up import isosceles_triangle_pointing_up
from patternlib.shapes.triangle.narrow_isosceles_triangle_pointing_up import narrow_isosceles_triangle_pointing_up
from patternlib.shapes.triangle.isosceles_triangle_pointing_down import isosceles_triangle_pointing_down
from patternlib.shapes.triangle.narrow_isosceles_triangle_pointing_down import narrow_isosceles_triangle_pointing_down
from patternlib.shapes.triangle.narrow_string_isosceles_triangle_pointing_up import narrow_string_isosceles_triangle_pointing_up
from patternlib.shapes.triangle.wide_string_isosceles_triangle_pointing_up import wide_string_isosceles_triangle_pointing_up
from patternlib.shapes.triangle.narrow_string_isosceles_triangle_pointing_down import narrow_string_isosceles_triangle_pointing_down
from patternlib.shapes.triangle.number_increasing_along_row_right_angle_triangle import number_increasing_along_row_right_angle_triangle
from patternlib.shapes.triangle.number_increasing_along_column_right_angle_triangle import number_increasing_along_column_right_angle_triangle
from patternlib.shapes.triangle.number_increasing_along_column_right_angle_triangle_inverted_across_hplane import number_increasing_along_column_right_angle_triangle_inverted_across_hplane
from patternlib.shapes.triangle.number_increasing_along_column_right_angle_triangle_inverted_across_h_and_v_plane import number_increasing_along_column_right_angle_triangle_inverted_across_h_and_v_plane
from patternlib.shapes.triangle.number_increasing_along_column_right_angle_triangle_inverted_across_vplane import number_increasing_along_column_right_angle_triangle_inverted_across_vplane
from patternlib.shapes.triangle.number_increasing_along_column_isosceles_triangle_pointing_up import number_increasing_along_column_isosceles_triangle_pointing_up
from patternlib.shapes.triangle.decreasing_number_triangle import decreasing_number_triangle
from patternlib.shapes.triangle.inverted_same_number_as_row_right_angle_triangle import inverted_same_number_as_row_right_angle_triangle
from patternlib.shapes.triangle.numbers_indicating_column_num_inverted import numbers_indicating_column_num_inverted
from patternlib.shapes.triangle.string_right_angle_triangle import string_right_angle_triangle
from patternlib.shapes.triangle.string_right_angle_triangle_inverted_across_hplane import string_right_angle_triangle_inverted_across_hplane
from patternlib.shapes.triangle.string_right_angle_triangle_inverted_across_vplane import string_right_angle_triangle_inverted_across_vplane
from patternlib.shapes.triangle.string_right_angle_triangle_inverted_across_h_and_v_plane import string_right_angle_triangle_inverted_across_h_and_v_plane

# Hour glass
from patternlib.shapes.hour_glass.horizontal_hour_glass import horizontal_hour_glass
from patternlib.shapes.hour_glass.horizontal_hour_glass_common_midpoint import horizontal_hour_glass_common_midpoint
from patternlib.shapes.hour_glass.hour_glass import hour_glass
from patternlib.shapes.hour_glass.string_hour_glass import string_hour_glass
from patternlib.shapes.hour_glass.hollow_hour_glass import hollow_hour_glass

# Diamond
from patternlib.shapes.diamond.wide_diamond import wide_diamond
from patternlib.shapes.diamond.narrow_diamond import narrow_diamond
from patternlib.shapes.diamond.narrow_string_diamond import narrow_string_diamond
from patternlib.shapes.diamond.wide_string_diamond import wide_string_diamond
from patternlib.shapes.diamond.hollow_diamond import hollow_diamond

# Pyramid
from patternlib.shapes.pyramid.pyramid_pointing_up import pyramid_pointing_up
from patternlib.shapes.pyramid.pyramid_pointing_down import pyramid_pointing_down
from patternlib.shapes.pyramid.hollow_pyramid_pointing_up import hollow_pyramid_pointing_up
from patternlib.shapes.pyramid.hollow_pyramid_pointing_down import hollow_pyramid_pointing_down
from patternlib.shapes.pyramid.increasing_number_pyramid_pointing_up import increasing_number_pyramid_pointing_up
from patternlib.shapes.pyramid.increasing_number_pyramid_pointing_down import increasing_number_pyramid_pointing_down
from patternlib.shapes.pyramid.string_pyramid_pointing_up import string_pyramid_pointing_up
from patternlib.shapes.pyramid.string_pyramid_pointing_down import string_pyramid_pointing_down
from patternlib.shapes.pyramid.decreasing_number_pyramid_pointing_up import decreasing_number_pyramid_pointing_up
from patternlib.shapes.pyramid.decreasing_number_pyramid_pointing_down import decreasing_number_pyramid_pointing_down

# Miscellaneous
from patternlib.shapes.miscellaneous.inverted_number_7 import inverted_number_7
from patternlib.shapes.miscellaneous.inverted_sigma import inverted_sigma
from patternlib.shapes.miscellaneous.inverted_z import inverted_z
from patternlib.shapes.miscellaneous.number_7 import number_7
from patternlib.shapes.miscellaneous.pyramid_diamond import pyramid_diamond
from patternlib.shapes.miscellaneous.pyramid_hour_glass import pyramid_hour_glass
from patternlib.shapes.miscellaneous.sigma import sigma


__all__ = [
    # ALPHABETS
    "l_pattern",
    "e_pattern",
    "h_pattern",
    "i_pattern",
    "t_pattern",
    "f_pattern",
    "a_pattern",
    "v_pattern",
    "x_pattern",
    "z_pattern",

    # SHAPES
    # Triangles
    "right_angle_triangle_pattern",
    "same_number_as_row_right_angle_triangle",
    "custom_string_right_angle_triangle",
    "string_triangle_pointing_right",
    "right_angle_triangle_inverted_across_hplane",
    "right_angle_triangle_inverted_across_h_and_v_plane",
    "right_angle_triangle_inverted_across_vplane",
    "triangle_pointing_right",
    "triangle_pointing_right_double_center_row",
    "triangle_pointing_left",
    "triangle_pointing_left_double_center_row",
    "isosceles_triangle_pointing_up",
    "narrow_isosceles_triangle_pointing_up",
    "isosceles_triangle_pointing_down",
    "narrow_string_isosceles_triangle_pointing_up",
    "wide_string_isosceles_triangle_pointing_up",
    "narrow_string_isosceles_triangle_pointing_down",
    "number_increasing_along_row_right_angle_triangle",
    "number_increasing_along_column_right_angle_triangle",
    "number_increasing_along_column_right_angle_triangle_inverted_across_hplane",
    "number_increasing_along_column_right_angle_triangle_inverted_across_h_and_v_plane",
    "number_increasing_along_column_right_angle_triangle_inverted_across_vplane",
    "number_increasing_along_column_isosceles_triangle_pointing_up",
    "inverted_same_number_as_row_right_angle_triangle",
    "decreasing_number_triangle",
    "numbers_indicating_column_num_inverted",
    "string_right_angle_triangle",
    "string_right_angle_triangle_inverted_across_hplane",
    "string_right_angle_triangle_inverted_across_vplane",
    "string_right_angle_triangle_inverted_across_h_and_v_plane",
    # Hour glass
    "horizontal_hour_glass",
    "horizontal_hour_glass_common_midpoint",
    "hour_glass",
    "string_hour_glass",
    "hollow_hour_glass",
    # Diamond
    "wide_diamond",
    "narrow_diamond",
    "narrow_string_diamond",
    "wide_string_diamond",
    "hollow_diamond",
    # Pyramid
    "pyramid_pointing_up",
    "pyramid_pointing_down",
    "hollow_pyramid_pointing_up",
    "hollow_pyramid_pointing_down",
    "increasing_number_pyramid_pointing_up",
    "increasing_number_pyramid_pointing_down",
    "string_pyramid_pointing_up",
    "string_pyramid_pointing_down",
    "decreasing_number_pyramid_pointing_up",
    "decreasing_number_pyramid_pointing_down",
    # Miscellaneous
    "inverted_number_7",
    "inverted_sigma",
    "inverted_z",
    "number_7",
    "pyramid_diamond",
    "pyramid_hour_glass",
    "sigma",
    "is_input_str"
]

str_patterns = [
    "narrow_string_isosceles_triangle_pointing_up",
    "custom_string_right_angle_triangle",
    "string_triangle_pointing_right",
    "narrow_string_isosceles_triangle_pointing_up",
    "wide_string_isosceles_triangle_pointing_up",
    "narrow_string_isosceles_triangle_pointing_down",
    "string_right_angle_triangle",
    "string_right_angle_triangle_inverted_across_hplane",
    "string_right_angle_triangle_inverted_across_vplane",
    "string_right_angle_triangle_inverted_across_vplane",
    "string_right_angle_triangle_inverted_across_h_and_v_plane",
    "string_hour_glass",
    "narrow_string_diamond",
    "wide_string_diamond",
    "string_pyramid_pointing_up",
    "string_pyramid_pointing_down",
]

def is_input_str(name):
    if name and name in str_patterns:
        return True
    return False


