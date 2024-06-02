from patternlib.constants.patternlib_constants import ROWS5

MINROW = 2

def hollow_pyramid_pointing_down(row=ROWS5):
    '''
    * * * * *
     *     *
      *   *
       * *
        *
    This generates a hollow pyramid pointing up.

    To view pattern run: 'print(hollow_pyramid_pointing_down.__doc__)'
    '''
    if row < MINROW:
        print("Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        for i in range(row, 0, -1):
            if i == row or i == 1:
                print(('* ' * i).center(2 * row))
            else:
                print(('* ' + '  ' * (i - 2) + '* ').center(2 * row))
        