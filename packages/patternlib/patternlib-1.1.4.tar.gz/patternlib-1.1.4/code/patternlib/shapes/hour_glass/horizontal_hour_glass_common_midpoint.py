from patternlib.constants.patternlib_constants import ROWS5

MINROW = 2

def horizontal_hour_glass_common_midpoint(row=ROWS5):
    '''
    *               *
    * *           * *
    * * *       * * *
    * * * *   * * * *
    * * * * * * * * *
    * * * *   * * * *
    * * *       * * *
    * *           * *
    *               *

    This generates a horizontal hour glass with the two mirrored triangles sharing a common midpoint.

    To view pattern run: 'print(horizontal_hour_glass_common_midpoint.__doc__)'
    '''
    if row < MINROW:
        print("Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        for i in range(1, 2 * row + 1):
            if i < row:
                print(('* ' * i).ljust(2 * row - 1) + (' *' * i).rjust(2 * row - 2))
            elif i == row:
                print(('* ' * (i - 1)).ljust(2 * row - 2) + '*' + ((' *' * (i - 1)).rjust(2 * row - 2)))
            else:
                print((('* ' * (2 * row - i)).ljust(2 * row - 1) + (' *' * (2 * row - i)).rjust(
                    2 * row - 2)))