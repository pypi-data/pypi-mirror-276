from patternlib.constants.patternlib_constants import ROWS3

MINROW = 2

def number_7(row=ROWS3):
    '''
    * * *
       *
      *
     *
    *

    This generates a pattern representing the number 7.

    To view pattern run: 'print(number_7.__doc__)'
    '''
    if row < MINROW:
        print("Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        for i in range(row, 0, -1):
            if i == row or i == 1:
                print(('* ' * i).center(2 * row))
            else:
                print(('  ' * (i - 1) + '* ').center(2 * row))
        for i in range(2, row + 1):
            if i == 1:
                print(('* ' * i).center(2 * row))
            else:
                print(('* ' + '  ' * (i - 1)).center(2 * row))
