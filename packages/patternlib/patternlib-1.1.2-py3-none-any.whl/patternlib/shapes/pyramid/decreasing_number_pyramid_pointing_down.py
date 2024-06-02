from patternlib.constants.patternlib_constants import ROWS5

MINROW = 2

def decreasing_number_pyramid_pointing_down(row=ROWS5):
    '''
    5   4   3   2   1
      4   3   2   1
        3   2   1
          2   1
            1

    This generates a pyramid pointing down made up of numbers decreasing from left to right.

    To view pattern run: 'print(decreasing_number_pyramid_pointing_down.__doc__)'
    '''
    if row < MINROW:
        print("Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        for i in range(row, 0, -1):
            res = ''
            for x in range(i, 0, -1):
                res += str(x).rjust(4)
            print(res.center(4 * row))