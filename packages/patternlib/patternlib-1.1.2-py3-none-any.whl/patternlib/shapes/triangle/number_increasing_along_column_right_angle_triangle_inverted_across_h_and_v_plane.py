from patternlib.constants.patternlib_constants import ROWS5, STARTING_POINT2

MINROW = 2

def number_increasing_along_column_right_angle_triangle_inverted_across_h_and_v_plane(row=ROWS5, starting_point=STARTING_POINT2):
    '''
    11 12 14 17 21
       13 15 18 22
          16 19 23
             20 24
                25

    This generates a right angle triangle with numbers increasing along its columns.
    The triangle is inverted across horizontal and vertical planes.

    To view pattern run: 'print(number_increasing_along_column_right_angle_triangle_inverted_across_h_and_v_plane.__doc__)'
    '''
    if row < MINROW:
        print("right-angled-triangle-Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        for i in range(row, 0, -1):
            starting_point = starting_point + row - i
            d = row - i + 1
            r = ' ' * 3 * (row - i) + str(starting_point) + ' '
            v = starting_point + d
            for x in range(0, i - 1):
                r = r + str(v) + ' '
                d += 1
                v += d
            print(r)
            starting_point += 1
