from patternlib.constants.patternlib_constants import ROWS5

MINROW = 2

def hour_glass(row=ROWS5):
    '''
    *********
     *******
      *****
       ***
        *
       ***
      *****
     *******
    *********

    This generates an hour glass.

    To view pattern run: 'print(hour_glass.__doc__)'
    '''
    if row < MINROW:
        print("Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        for i in range(row, 0, -2):
            print(('*' * i).center(1 * row))
        for i in range(3 if row % 2 == 1 else 2, row + 1, 2):
            print(('*' * i).center(1 * row))