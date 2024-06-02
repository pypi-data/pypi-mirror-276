from patternlib.constants.patternlib_constants import ROWS5

MINROW = 3

def t_pattern(row=ROWS5):
    '''
    * * *
      *
      *
      *
      *

    This generates T - Pattern.

    To view pattern run: 'print(t_pattern.__doc__)'
    '''
    if row < MINROW:
        print("L-Pattern generation failed, number of rows has to be greater than 1...")
    else:
        halfway = row // 2 + 1
        for i in range(1, row + 1):
            if i == 1:
                print("* " * halfway)
            else:
                print("*".center(row))