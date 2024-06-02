from patternlib.constants.patternlib_constants import ROWS5

MINROW = 2

def triangle_pointing_right(row=ROWS5):
    '''
    *
    * *
    * * *
    * * * *
    * * * * *
    * * * *
    * * *
    * *
    *

    This generates a triangle pointing to the right with the fill character *

    To view pattern run: 'print(triangle_pointing_right.__doc__)'
    '''
    if row < MINROW:
        print("Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        for i in range(1, 2 * row + 1):
            print('* ' * i) if i <= row else print('* ' * (2 * row - i))