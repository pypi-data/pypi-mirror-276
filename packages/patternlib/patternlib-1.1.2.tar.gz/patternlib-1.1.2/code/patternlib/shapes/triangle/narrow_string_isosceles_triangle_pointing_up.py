from patternlib.constants.patternlib_constants import ALPHABETS_STRING

MINROW = 2

def narrow_string_isosceles_triangle_pointing_up(string=ALPHABETS_STRING):
    '''
        A
       ABA
      ABCBA
     ABCDCBA
    ABCDEDCBA

    This generates a narrow isosceles triangle made of alphabets pointing up.

    To view pattern run: 'print(narrow_string_isosceles_triangle_pointing_up.__doc__)'
    '''
    if len(string) < MINROW:
        print("Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        for i in range(0, len(string)):
            print((string[0: i + 1] + string[i - (len(string) + 1):: -1]).center(2 * len(string)))