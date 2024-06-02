from patternlib.constants.patternlib_constants import ROWS5

MINROW = 2

def isosceles_triangle_pointing_up(row=ROWS5):
    '''
                 *
              *  *  *
           *  *  *  *  *
        *  *  *  *  *  *  *
     *  *  *  *  *  *  *  *  * 

    This generates an isosceles triangle pointing up with the fill character *

    To view pattern run: 'print(isosceles_triangle_pointing_up.__doc__)'
    '''
    if row < MINROW:
        print("Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        for i in range(1, 2 * row + 1, 2):
            print((' * ' * i).center(6 * row - 3))
