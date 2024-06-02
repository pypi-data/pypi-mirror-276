from patternlib.constants.patternlib_constants import ROWS5

MINROW = 2

def pyramid_pointing_up(row=ROWS5):
    '''
        *
       * *
      * * *
     * * * *
    * * * * *

    This generates a pyramid pointing up.

    To view pattern run: 'print(pyramid_pointing_up.__doc__)'
    '''
    if row < MINROW:
        print("Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        for i in range(1, row + 1):
            print(('* ' * i).center(2 * row))