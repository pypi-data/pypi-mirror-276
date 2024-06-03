from patternlib.constants.patternlib_constants import ROWS5

MINROW = 2

def increasing_number_pyramid_pointing_up(row=ROWS5):
    '''
            1
          1   2
        1   2   3
      1   2   3   4
    1   2   3   4   5

    This generates a pyramid pointing up made up of numbers increasing from left to right.

    To view pattern run: 'print(increasing_number_pyramid_pointing_up.__doc__)'
    '''
    if row < MINROW:
        print("Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        for i in range(1, row + 1):
            res = ''
            for x in range(1, i + 1):
                res += str(x).rjust(4)
            print(res.center(4 * row))