from patternlib.constants.patternlib_constants import ROWS5

MINROW = 2

def narrow_diamond(row=ROWS5):
    '''
        *
       ***
      *****
     *******
    *********
     *******
      *****
       ***
        *

    This generates a narrow diamond pattern.

    To view pattern run: 'print(narrow_diamond.__doc__)'
    '''
    if row < MINROW:
        print("Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        for i in range(1, 2 * row + 1, 2):
            if i <= row:
                print(('*' * i).center(1 * row))
            else:
                print(('*' * (2 * row - i)).center(1 * row))