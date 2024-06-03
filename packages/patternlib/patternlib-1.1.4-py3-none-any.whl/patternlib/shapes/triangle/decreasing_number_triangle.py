from patternlib.constants.patternlib_constants import ROWS5

MINROW = 2

def decreasing_number_triangle(row=ROWS5):
    '''
    1
    2  1
    3  2  1
    4  3  2  1
    5  4  3  2  1

    This generates right-angled-triangle-pattern with numbers in its rows printed in decreasing order

    To view pattern run: 'print(decreasing_number_triangle.__doc__)'
    '''
    if row < MINROW:
        print("right-angled-triangle-Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        for i in range(1, row + 1):
            res = ''
            for x in range(i, 0, -1):
                res += str(x).rjust(3)
            print(res)