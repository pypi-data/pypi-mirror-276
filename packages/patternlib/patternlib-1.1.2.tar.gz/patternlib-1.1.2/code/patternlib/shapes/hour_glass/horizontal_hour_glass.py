from patternlib.constants.patternlib_constants import ROWS5

MINROW = 2

def horizontal_hour_glass(row=ROWS5):
    '''
    *                  *
    * *              * *
    * * *          * * *
    * * * *      * * * *
    * * * * *  * * * * *
    * * * *      * * * *
    * * *          * * *
    * *              * *
    *                  *

    This generates a horizontal hour glass.

    To view pattern run: 'print(horizontal_hour_glass.__doc__)'
    '''
    if row < MINROW:
        print("Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        for i in range(1, 2 * row + 1):
            print(('* ' * i).ljust(2 * row) + (' *' * i).rjust(2 * row)) if i <= row else print(
                ('* ' * (2 * row - i)).ljust(2 * row) + (' *' * (2 * row - i)).rjust(2 * row))