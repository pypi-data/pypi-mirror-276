from patternlib.constants.patternlib_constants import ROWS5, STARTING_POINT

MINROW = 2

def number_increasing_along_row_right_angle_triangle(row=ROWS5, starting_point=STARTING_POINT):
    '''
       1
       2    3
       4    5    6
       7    8    9   10
      11   12   13   14   15

    This generates a right angle triangle with numbers increasing along its rows.

    To view pattern run: 'print(number_increasing_along_row_right_angle_triangle.__doc__)'
    '''

    if row < MINROW:
        print("right-angled-triangle-Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        for i in range(1, row + 1):
            for x in range(i):
                print(str(starting_point).rjust(4), end=" ")
                starting_point += 1
            print()
