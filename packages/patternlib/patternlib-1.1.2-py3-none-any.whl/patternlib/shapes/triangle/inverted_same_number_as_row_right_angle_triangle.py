from patternlib.constants.patternlib_constants import ROWS5

MINROW = 2

def inverted_same_number_as_row_right_angle_triangle(row=ROWS5):
    '''
      1  1  1  1  1
         2  2  2  2
            3  3  3
               4  4
                  5

    To view pattern run: 'print(inverted_same_number_as_row_right_angle_triangle.__doc__)'
    '''
    if row < MINROW:
        print("right-angled-triangle-Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        for i in range(1, row + 1):
            res = ''
            for x in range(i, row + 1):
                res += str(i).rjust(3)
            print(res.rjust(3 * row))