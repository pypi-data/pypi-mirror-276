from patternlib.constants.patternlib_constants import ROWS5

MINROW = 3


def f_pattern(row=ROWS5):
    """
    * * *
    *
    * *
    *
    *

    This generates F-Pattern

    To view pattern run: 'print(f_pattern.__doc__)'
    """
    if row < MINROW:
        print("E-Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        halfway = row // 2 + 1
        for i in range(1, row + 1):
            if i == 1:
                print('* ' * halfway)
            elif i == halfway:
                print('* ' * (halfway - 1))
            else:
                print('*')

