from patternlib.constants.patternlib_constants import ALPHABETS_STRING

MINROW = 2

def string_hour_glass(string=ALPHABETS_STRING):
    '''
    ABCDEDCBA
     ABCDCBA
      ABCBA
       ABA
        A
       ABA
      ABCBA
     ABCDCBA
    ABCDEDCBA

    This generates an hour glass made of characters of the input string.

    To view pattern run: 'print(string_hour_glass.__doc__)'
    '''
    if len(string) < MINROW:
        print("Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        for i in range(len(string) - 1, -1, -1):
            print((string[0:i + 1] + string[i - (len(string) + 1):: -1]).center(2 * len(string)))
        for i in range(1, len(string)):
            print((string[0: i + 1] + string[i - (len(string) + 1):: -1]).center(2 * len(string)))