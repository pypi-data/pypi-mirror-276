from patternlib.constants.patternlib_constants import ROWS5, STARTING_POINT2

MINROW = 2

def number_increasing_along_column_isosceles_triangle_pointing_up(row=ROWS5, starting_point=STARTING_POINT2):
    '''
                25
             20 24 29
          16 19 23 28 32
       13 15 18 22 27 31 36
    11 12 14 17 21 26 30 35 39
    This generates an isosceles triangle with numbers increasing along its columns.

    To view pattern run: 'print(number_increasing_along_column_isosceles_triangle_pointing_up.__doc__)'
    '''
    if row < MINROW:
        print("right-angled-triangle-Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        for i in range(1, row + 1):
            d = row - i + 1
            r = ' ' * 3 * (row - i) + str(starting_point) + ' '
            v = starting_point + d
            for x in range(2 * i - 2):
                r = r + str(v) + ' '
                if d == 5:
                    d -= 1
                else:
                    d += 1
                v += d
            print(r)
            starting_point = starting_point - (row + 1 - i)

