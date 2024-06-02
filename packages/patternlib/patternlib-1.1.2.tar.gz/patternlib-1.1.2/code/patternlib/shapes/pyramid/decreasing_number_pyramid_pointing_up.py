from patternlib.constants.patternlib_constants import ROWS5

MINROW = 2

def decreasing_number_pyramid_pointing_up(row=ROWS5):
    '''
            1
          2   1
        3   2   1
      4   3   2   1
    5   4   3   2   1

    This generates a pyramid pointing up made up of numbers decreasing from left to right.

    To view pattern run: 'print(decreasing_number_pyramid_pointing_up.__doc__)'
    '''
    if row < MINROW:
        print("Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        for i in range(1, row + 1):
            res = ''
            for x in range(i, 0, -1):
                res += str(x).rjust(4)
            print(res.center(4 * row))
