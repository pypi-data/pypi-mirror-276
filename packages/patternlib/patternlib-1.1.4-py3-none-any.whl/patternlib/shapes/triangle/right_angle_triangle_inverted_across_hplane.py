from patternlib.constants.patternlib_constants import ROWS5

MINROW = 2

def right_angle_triangle_inverted_across_hplane(row=ROWS5):
    '''
    * * * * *
    * * * *
    * * *
    * *
    *

    This generates right-angled-triangle-pattern inverted across the horizontal plane.

    To view pattern run: 'print(right_angle_triangle_inverted_across_hplane.__doc__)'
    '''
    if row < MINROW:
        print("Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        for i in range(row, 0, -1):
            print("* " * i)