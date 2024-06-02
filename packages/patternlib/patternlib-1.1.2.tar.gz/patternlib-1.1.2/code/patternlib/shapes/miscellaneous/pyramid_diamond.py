from patternlib.constants.patternlib_constants import ROWS5

MINROW = 2

def pyramid_diamond(row=ROWS5):
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

    This generates a diamond constituted of pyramids.

    To view pattern run: 'print(inverted_sigma.__doc__)'
    '''
    if row < MINROW:
        print("Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        for i in range(1, row + 1):
            print(('* ' * i).center(2 * row))
        for i in range(row - 1, 0, -1):
            print(('* ' * i).center(2 * row))
        
