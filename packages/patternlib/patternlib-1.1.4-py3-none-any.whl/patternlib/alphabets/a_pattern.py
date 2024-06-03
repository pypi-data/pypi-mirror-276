from patternlib.constants.patternlib_constants import ROWS5

MINROW = 3


def a_pattern(rows=ROWS5):
    '''
        *
       * *
      * * *
     *     *
    *       *

    This generates A - Pattern.

    To view pattern run: 'print(a_pattern.__doc__)'
    '''
    if rows < MINROW:
        print("E-Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        mid = rows // 2 + 1
        for i in range(1, rows + 1):
            if i == mid or i == 1:
                print(('* ' * i).center(2 * rows))
            else:
                print(('* ' + '  ' * (i - 2) + '* ').center(2 * rows))