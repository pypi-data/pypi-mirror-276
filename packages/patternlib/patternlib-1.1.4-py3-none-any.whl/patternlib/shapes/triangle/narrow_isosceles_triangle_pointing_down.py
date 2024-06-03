from patternlib.constants.patternlib_constants import ROWS5

MINROW = 2

def narrow_isosceles_triangle_pointing_down(row=ROWS5):
    '''
    *********
     *******
      *****
       ***
        *

    This generates a narrow isosceles triangle pointing down with the fill character *

    To view pattern run: 'print(narrow_isosceles_triangle_pointing_down.__doc__)'
    '''
    if row < MINROW:
        print("Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        for i in range(2 * row - 1, 0, -2):
            print(('*' * i).center(2 * row - 1))