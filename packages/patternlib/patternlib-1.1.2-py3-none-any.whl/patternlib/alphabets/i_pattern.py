from patternlib.constants.patternlib_constants import ROWS5

MINROW = 3

def i_pattern(row=ROWS5):
    '''
    * * *
      *
      *
      *
    * * *

    This generates I - Pattern.

    To view pattern run: 'print(i_pattern.__doc__)'
    '''
    if row < MINROW:
        print("E-Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        halfway = row // 2 + 1
        for i in range(1, row + 1):
            if 1 < i < row:
                print("*".center(row))
            else:
                print("* " * halfway)

