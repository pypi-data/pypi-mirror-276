from patternlib.constants.patternlib_constants import ROWS5

MINROW = 2

def pyramid_hour_glass(row=ROWS5):
    '''
    * * * * *
     * * * *
      * * *
       * *
        *
       * *
      * * *
     * * * *
    * * * * *

    This generates an hour glass made up of pyramids.

    To view pattern run: 'print(pyramid_hour_glass.__doc__)'
    '''
    if row < MINROW:
        print("Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        for i in range(row, 0, -1):
            print(('* ' * i).center(2 * row))
        for i in range(2, row + 1):
            print(('* ' * i).center(2 * row))
