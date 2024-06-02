from patternlib.constants.patternlib_constants import ROWS5

MINROW = 2

def hollow_hour_glass(row=ROWS5):
    '''
    * * * * *
     *     *
      *   *
       * *
        *
       * *
      *   *
     *     *
    * * * * *

    This generates a hollow hour glass.

    To view pattern run: 'print(hollow_hour_glass.__doc__)'
    '''
    if row < MINROW:
        print("Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        for i in range(row, 0, -1):
            if i == row or i == 1:
                print(('* ' * i).center(2 * row))
            else:
                print(('* ' + '  ' * (i - 2) + '* ').center(2 * row))
        for i in range(2, row + 1):
            if i == row or i == 1:
                print(('* ' * i).center(2 * row))
            else:
                print(('* ' + '  ' * (i - 2) + '* ').center(2 * row))