from patternlib.constants.patternlib_constants import ROWS5, REVERSE_STARTING_POINT

MINROW = 2

def number_increasing_along_column_right_angle_triangle_inverted_across_vplane(row=ROWS5, starting_point=REVERSE_STARTING_POINT):
    '''
                25
             20 24
          16 19 23
       13 15 18 22
    11 12 14 17 21
    This generates a right angle triangle with numbers increasing along its columns.
    The triangle is inverted across a vertical plane.

    To view pattern run: 'print(number_increasing_along_column_right_angle_triangle_inverted_across_vplane.__doc__)'
    '''
    if row < MINROW:
        print("right-angled-triangle-Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        for i in range(1, row + 1):
            d = row - i + 1
            r = ' ' * 3 * (row - i) + str(starting_point) + ' '
            v = starting_point + d
            for x in range(i - 1):
                r = r + str(v) + ' '
                d += 1
                v += d
            print(r)
            starting_point = starting_point - (row + 1 - i)


