from patternlib.constants.patternlib_constants import ROWS5, STARTING_POINT

MINROW = 2

def number_increasing_along_column_right_angle_triangle_inverted_across_hplane(row=ROWS5, starting_point=STARTING_POINT):
    '''
    19  24  28  31  33
    20  25  29  32
    21  26  30
    22  27
    23

    This generates a right angle triangle with numbers increasing along its columns.
    The triangle is inverted across a horizontal plane.

    To view pattern run: 'print(number_increasing_along_column_right_angle_triangle_inverted_across_hplane.__doc__)'
    '''
    if row < MINROW:
        print("right-angled-triangle-Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        a = [i for i in range(row, 1, -1)]
        for i in range(row, -1, -1):
            for x in range(i):
                if x == 0:
                    print(str(starting_point).rjust(3), end=' ')
                else:
                    y = starting_point + sum(a[:x])
                    print(str(y).rjust(3), end=' ')
            starting_point += 1
            print()
