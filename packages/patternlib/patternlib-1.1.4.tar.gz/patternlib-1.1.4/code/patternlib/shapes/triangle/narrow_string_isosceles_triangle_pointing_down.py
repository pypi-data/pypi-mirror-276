from patternlib.constants.patternlib_constants import ALPHABETS_STRING

MINROW = 2

def narrow_string_isosceles_triangle_pointing_down(string=ALPHABETS_STRING):
    '''
    ABCDEDCBA
     ABCDCBA
      ABCBA
       ABA
        A

    This generates a narrow isosceles triangle made of alphabets pointing down.

    To view pattern run: 'print(narrow_string_isosceles_triangle_pointing_down.__doc__)'
    '''
    if len(string) < MINROW:
        print("Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        for i in range(len(string) - 1, -1, -1):
            print((string[0:i + 1] + string[i - (len(string) + 1):: -1]).center(2 * len(string)))


