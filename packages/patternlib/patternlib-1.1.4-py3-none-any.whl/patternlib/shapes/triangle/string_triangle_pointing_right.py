# This generates an isosceles triangle pattern pointing to the right.
# It contains the letters from the string provided as the argument.
# The number of characters first increase up till the length of the entire string then decrease.
# P
# P Y
# P Y T
# P Y T H
# P Y T H O
# P Y T H O N
# P Y T H O
# P Y T H
# P Y T
# P Y
# P

from patternlib.constants.patternlib_constants import STD_STRING1

MINROW = 2

def string_triangle_pointing_right(input_string=STD_STRING1):
    '''
    P
    P Y
    P Y T
    P Y T H
    P Y T H O
    P Y T H O N
    P Y T H O
    P Y T H
    P Y T
    P Y
    P

    To view pattern run: 'print(string_triangle_pointing_right.__doc__)'
    '''
    if len(input_string) <= MINROW:
        print("right-angled-triangle-Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        index_count = 0
        while index_count < len(input_string):
            print(" ".join(char.upper() for char in input_string[0: index_count + 1]))
            index_count += 1
        index_count -= 2
        while index_count >= 0:
            print(" ".join(char.upper() for char in input_string[0: index_count + 1]))
            index_count -= 1