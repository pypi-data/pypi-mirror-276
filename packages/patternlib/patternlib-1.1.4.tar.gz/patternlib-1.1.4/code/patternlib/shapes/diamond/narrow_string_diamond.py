from patternlib.constants.patternlib_constants import ALPHABETS_STRING

MINROW = 2

def narrow_string_diamond(string=ALPHABETS_STRING):
    '''
        A
       ABA
      ABCBA
     ABCDCBA
    ABCDEDCBA
     ABCDCBA
      ABCBA
       ABA
        A

    This generates a narrow diamond made of alphabets.

    To view pattern run: 'print(narrow_string_diamond.__doc__)'
    '''
    if len(string) < MINROW:
        print("Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        for i in range(0, len(string)):
            print((string[0: i + 1] + string[i - (len(string) + 1):: -1]).center(2 * len(string)))
        for i in range(len(string) - 2, -1, -1):
            print((string[0: i + 1] + string[i - (len(string) + 1):: -1]).center(2 * len(string)))


