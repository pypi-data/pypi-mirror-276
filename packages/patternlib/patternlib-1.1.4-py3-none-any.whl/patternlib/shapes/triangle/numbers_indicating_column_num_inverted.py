from patternlib.constants.patternlib_constants import ROWS5

MINROW = 2

def numbers_indicating_column_num_inverted(row=ROWS5):
    '''
      1  2  3  4  5
         2  3  4  5
            3  4  5
               4  5
                  5

    This generates right-angled-triangle-pattern where each number indicates its column number.

    To view pattern run: 'print(numbers_indicating_column_num_inverted.__doc__)'
    '''
    if row < MINROW:
        print("right-angled-triangle-Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        for i in range(1, row + 1):
            res = ''
            for x in range(i, row + 1):
                res += str(x).rjust(3)
            print(res.rjust(3 * row))