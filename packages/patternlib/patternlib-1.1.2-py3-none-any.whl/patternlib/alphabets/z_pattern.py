from patternlib.constants.patternlib_constants import ROWS3

MINROW = 3


def z_pattern(rows=ROWS3):
    '''
            *
           * *
          * * *
         *     *
        *       *

        This generates Z - Pattern.

        To view pattern run: 'print(z_pattern.__doc__)'
        '''
    if rows < MINROW:
        print("E-Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        for i in range(rows, 0, -1):
            if i == rows or i == 1:
                print(('* ' * i).center(2 * rows))
            else:
                print(('  ' * (i - 1) + '* ').center(2 * rows))
        for i in range(2, rows + 1):
            if i == rows or i == 1:
                print(('* ' * i).center(2 * rows))
            else:
                print(('* ' + '  ' * (i - 1)).center(2 * rows))